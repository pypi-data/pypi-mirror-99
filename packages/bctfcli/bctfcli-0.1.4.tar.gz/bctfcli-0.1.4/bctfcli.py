import typer
import requests
import pydantic
import datetime
import humanize
import tempfile
import logging
import coloredlogs
import base64
import tabulate
import pathlib
import os
import subprocess
from typing import List
from typing_extensions import Literal

logger = logging.getLogger("bctfcli")
coloredlogs.install(level="INFO")

app = typer.Typer()

kLatestRoundUrl = "http://180.76.69.154:8090/latest_round.json"
kSubmitUrl = "http://180.76.69.154:8090/submit_redirect.php"
kSubmitResultUrl = "https://anquan.baidu.com/bctf/submit_result.php"


def parse_weird_time(v):
    v = v.replace("UTC+8", "CST")
    return datetime.datetime.strptime(v, r"%Y-%m-%d %H:%M:%S %Z")


class Challenge(pydantic.BaseModel):
    cb_id: str
    score: int
    score_method: Literal["Crash", "PopCalc"]
    cb_url: pydantic.AnyUrl
    cb_provider: str


class ScoreboardItem(pydantic.BaseModel):
    score: float
    first_blood: int
    bugs: int
    rank: int
    team: str
    robot: bool
    inhub: bool


class RoundInfo(pydantic.BaseModel):
    Start: datetime.datetime
    End: datetime.datetime
    CurrentRound: int
    CurrentChallenge: List[Challenge]
    scoreboard: List[ScoreboardItem]

    @pydantic.validator("Start", "End", pre=True)
    def parse_start_end_time(cls, v):
        return parse_weird_time(v)


class Payload(pydantic.BaseModel):
    ChallengeID: str
    Crash: str


class SubmitAnswerRequest(pydantic.BaseModel):
    RoundID: int
    Payload: Payload


class SubmitResultItem(pydantic.BaseModel):
    round_id: int
    cb_id: str
    score: float
    status: str
    submit_time: datetime.datetime

    @pydantic.validator("submit_time", pre=True)
    def parse_submit_time(cls, v):
        return parse_weird_time(v)


class SubmitResult(pydantic.BaseModel):
    team: str
    result: List[SubmitResultItem]


class Config(pydantic.BaseSettings):
    username: str
    password: str

    class Config:
        env_file = str(
            pathlib.Path(typer.get_app_dir("bctfcli", force_posix=True)) / "config"
        )
        env_file_encoding = "utf-8"
        env_prefix = "bctf_"


config = Config()
session = requests.session()
session.auth = (config.username, config.password)


def fetch_api(url, resp_model):
    r = session.get(url)
    if r.status_code != 200:
        typer.secho(r.status_code, fg="red")
        typer.secho(r.text, fg="red")
        raise ValueError()
    try:
        return resp_model.parse_raw(r.text)
    except pydantic.ValidationError:
        logger.error(f"unexpected server response from {url}: {r.text}")
        raise


def fetch_latest_round_info():
    return fetch_api(kLatestRoundUrl, RoundInfo)


def fetch_submit_result():
    return fetch_api(kSubmitResultUrl, SubmitResult)


def submit_answer(round_id: int, challenge_id: str, payload: bytes):
    req = SubmitAnswerRequest(
        RoundID=round_id, Payload=Payload(ChallengeID=challenge_id, Crash=base64.b64encode(payload))
    )
    print(req.json())
    r = session.post(kSubmitUrl, data=req.json())
    if r.status_code != 200:
        typer.secho(r.status_code, fg="red")
        typer.secho(r.text, fg="red")
        raise ValueError()
    logger.info(f"Submit answer result: {r.text}")


def infer_cb_id_by_cwd():
    cwd = os.getcwd()
    segments = cwd.split("/")
    if "chal" in segments:
        idx = segments.index("chal") + 1
        if idx < len(segments):
            return segments[idx]
    typer.secho("Please specify CB ID by --cb-id", fg="red")
    raise typer.Abort()


@app.command()
def submit(
    payload: typer.FileBinaryRead, cb_id: str = typer.Argument(infer_cb_id_by_cwd)
):
    def strip_prefix(v, prefix):
        if v.startswith(prefix):
            v = v[len(prefix) :]
        return v

    cb_id = strip_prefix(cb_id, "PopCalc_")
    cb_id = strip_prefix(cb_id, "Crash_")
    round_info = fetch_latest_round_info()
    for chal in round_info.CurrentChallenge:
        if chal.cb_id == cb_id:
            break
    else:
        typer.secho(f"No such challenge: {cb_id}", fg="red")
        raise typer.Abort()

    rid = round_info.CurrentRound
    payload = payload.read()
    typer.confirm(
        f"Going to submit answer for {cb_id}, round id = {rid}, payload length {len(payload)} bytes, confirm?",
        abort=True,
    )
    submit_answer(rid, cb_id, payload)


@app.command()
def info(url: bool = False):
    round_info = fetch_latest_round_info()
    typer.echo(f"Round {round_info.CurrentRound}:")
    typer.echo(
        f"Round starts at:\t{round_info.Start} ({humanize.naturaltime(round_info.Start)})"
    )
    typer.echo(
        f"Round ends at:  \t{round_info.End} ({humanize.naturaltime(round_info.End)})"
    )
    typer.echo("Challenges:")
    rows = []
    header = ["ID", "Type", "Score", "Author"]
    if url:
        header.append("URL")
    for chal in round_info.CurrentChallenge:
        cur = (chal.cb_id, chal.score_method, chal.score, chal.cb_provider)
        if url:
            cur += (chal.cb_url,)
        rows.append(cur)
    typer.echo(tabulate.tabulate(rows, headers=header))


@app.command()
def scoreboard():
    round_info = fetch_latest_round_info()
    typer.echo(f"Scoreboard at round {round_info.CurrentRound}:")
    typer.echo(
        tabulate.tabulate(
            [
                (
                    item.rank,
                    item.team,
                    item.score,
                    item.bugs,
                    item.first_blood,
                    item.robot,
                    item.inhub,
                )
                for item in round_info.scoreboard
            ],
            headers=[
                "Rank",
                "Name",
                "Score",
                "#Success",
                "#FirstBlood",
                "Is Robot",
                "In BotHub",
            ],
        )
    )


@app.command()
def download():
    cb_root = pathlib.Path("chal")
    archive_root = pathlib.Path("archive")
    round_info = fetch_latest_round_info()
    cb_root.mkdir(parents=True, exist_ok=True)
    archive_root.mkdir(parents=True, exist_ok=True)
    for chal in round_info.CurrentChallenge:
        to = cb_root / chal.cb_id
        if to.exists():
            logger.info(f"{to} already exists, skipped")
            continue
        tarpath = archive_root / chal.cb_url.split("/")[-1]
        with open(tarpath, "wb") as fp:
            logger.info(f"Downloading {chal.cb_url} to {tarpath}")
            fp.write(requests.get(chal.cb_url).content)
        logger.info(f"Extracting to {to}")
        with tempfile.TemporaryDirectory(dir=to.parent) as tmpd:
            subprocess.check_call(["tar", "-xvf", str(tarpath), "-C", str(tmpd)])
            pathlib.Path(tmpd).rename(to)


@app.command()
def result():
    results = fetch_submit_result()
    typer.echo(f"Submissions of team {results.team}:")
    typer.echo(
        tabulate.tabulate(
            [
                (item.round_id, item.cb_id, item.status, item.score, item.submit_time)
                for item in results.result
            ],
            headers=["Round", "CB ID", "Status", "Score", "Time"],
        )
    )


if __name__ == "__main__":
    app()
