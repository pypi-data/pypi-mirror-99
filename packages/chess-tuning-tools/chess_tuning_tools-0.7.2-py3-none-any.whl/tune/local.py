import pathlib
import re
import subprocess

import numpy as np
from scipy.stats import dirichlet
from skopt.space import Categorical, Integer, Real

from tune.utils import TimeControl

__all__ = [
    "run_match",
    "parse_experiment_result",
    "reduce_ranges",
    "elo_to_prob",
    "prob_to_elo",
]


def elo_to_prob(elo, k=4.0):
    """Convert an Elo score (logit space) to a probability.

    Parameters
    ----------
    elo : float
        A real-valued Elo score.
    k : float, optional (default=4.0)
        Scale of the logistic distribution.

    Returns
    -------
    float
        Win probability

    Raises
    ------
    ValueError
        if k <= 0

    """
    if k <= 0:
        raise ValueError("k must be positive")
    return 1 / (1 + np.power(10, -elo / k))


def prob_to_elo(p, k=4.0):
    """Convert a win probability to an Elo score (logit space).

    Parameters
    ----------
    p : float
        The win probability of the player.
    k : float, optional (default=4.0)
        Scale of the logistic distribution.

    Returns
    -------
    float
        Elo score of the player

    Raises
    ------
    ValueError
        if k <= 0

    """
    if k <= 0:
        raise ValueError("k must be positive")
    return k * np.log10(-p / (p - 1))


def parse_experiment_result(
    outstr,
    prior_counts=None,
    n_dirichlet_samples=1000000,
    score_scale=4.0,
    random_state=None,
    **kwargs,
):
    """Parse cutechess-cli result output to extract mean score and error.

    Here we use a simple pentanomial model to exploit paired openings.
    We distinguish the outcomes WW, WD, WL/DD, LD and LL and apply the
    following scoring (note, that the optimizer always minimizes the score):

    +------+------+-------+-----+-----+
    | WW   | WD   | WL/DD | LD  | LL  |
    +======+======+=======+=====+=====+
    | -1.0 | -0.5 | 0.0   | 0.5 | 1.0 |
    +------+------+-------+-----+-----+

    Note: It is important that the match output was produced using
    cutechess-cli using paired openings, otherwise the returned score is
    useless.

    Parameters
    ----------
    output : string (utf-8)
        Match output of cutechess-cli. It assumes the output was coming from
        a head-to-head match with paired openings.
    prior_counts : list-like float or int, default=None
        Pseudo counts to use for WW, WD, WL/DD, LD and LL in the
        pentanomial model.
    n_dirichlet_samples : int, default = 1 000 000
        Number of samples to draw from the Dirichlet distribution in order to
        estimate the standard error of the score.
    score_scale : float, optional (default=4.0)
        Scale of the logistic distribution used to calculate the score. Has to be a
        positive real number
    random_state : int, RandomState instance or None, optional (default: None)
        The generator used to initialize the centers. If int, random_state is
        the seed used by the random number generator; If RandomState instance,
        random_state is the random number generator; If None, the random number
        generator is the RandomState instance used by `np.random`.
    Returns
    -------
    score : float (in [-1, 1])
        Expected (negative) score of the first player (the lower the stronger)
    error : float
        Estimated standard error of the score. Estimated by repeated draws
        from a Dirichlet distribution.
    """
    wdl_strings = re.findall(r"Score of.*:\s*([0-9]+\s-\s[0-9]+\s-\s[0-9]+)", outstr)
    array = np.array(
        [np.array([int(y) for y in re.findall(r"[0-9]+", x)]) for x in wdl_strings]
    )
    diffs = np.diff(array, axis=0, prepend=np.array([[0, 0, 0]]))

    counts = {"WW": 0, "WD": 0, "WL/DD": 0, "LD": 0, "LL": 0}
    for i in range(0, len(diffs) - 1, 2):
        match = diffs[i] + diffs[i + 1]
        if match[0] == 2:
            counts["WW"] += 1
        elif match[0] == 1:
            if match[1] == 1:
                counts["WL/DD"] += 1
            else:
                counts["WD"] += 1
        elif match[1] == 1:
            counts["LD"] += 1
        elif match[2] == 2:
            counts["WL/DD"] += 1
        else:
            counts["LL"] += 1
    counts_array = np.array(list(counts.values()))
    if prior_counts is None:
        prior_counts = np.array([0.14, 0.19, 0.34, 0.19, 0.14]) * 2.5
    elif len(prior_counts) != 5:
        raise ValueError("Argument prior_counts should contain 5 elements.")
    dist = dirichlet(alpha=counts_array + prior_counts)
    scores = [0.0, 0.25, 0.5, 0.75, 1.0]
    score = prob_to_elo(dist.mean().dot(scores), k=score_scale)
    error = prob_to_elo(
        dist.rvs(n_dirichlet_samples, random_state=random_state).dot(scores),
        k=score_scale,
    ).var()
    return score, error


def _construct_engine_conf(
    id,
    engine_npm=None,
    engine_tc=None,
    engine_st=None,
    engine_ponder=False,
    timemargin=None,
):
    result = ["-engine", f"conf=engine{id}"]
    if engine_npm is not None:
        result.extend(("tc=inf", f"nodes={engine_npm}"))
        return result
    if engine_st is not None:
        result.append(f"st={str(engine_st)}")
        if timemargin is not None:
            result.append(f"timemargin={str(timemargin)}")
        if engine_ponder:
            result.append("ponder")
        return result
    if isinstance(engine_tc, str):
        engine_tc = TimeControl.from_string(engine_tc)
    result.append(f"tc={str(engine_tc)}")
    if timemargin is not None:
        result.append(f"timemargin={str(timemargin)}")
    if engine_ponder:
        result.append("ponder")
    return result


def run_match(
    rounds=10,
    engine1_tc=None,
    engine2_tc=None,
    engine1_st=None,
    engine2_st=None,
    engine1_npm=None,
    engine2_npm=None,
    engine1_ponder=False,
    engine2_ponder=False,
    timemargin=None,
    opening_file=None,
    adjudicate_draws=False,
    draw_movenumber=1,
    draw_movecount=10,
    draw_score=8,
    adjudicate_resign=False,
    resign_movecount=3,
    resign_score=550,
    adjudicate_tb=False,
    tb_path=None,
    concurrency=1,
    debug_mode=False,
    **kwargs,
):
    """Run a cutechess-cli match of two engines with paired random openings.

    Parameters
    ----------
    rounds : int, default=10
        Number of rounds to play in the match (each round consists of 2 games).
    engine1_tc : str or TimeControl object, default=None
        Time control to use for the first engine. If str, it can be a
        non-increment time control like "10" (10 seconds) or an increment
        time control like "5+1.5" (5 seconds total with 1.5 seconds increment).
        If None, it is assumed that engine1_npm or engine1_st is provided.
    engine2_tc : str or TimeControl object, default=None
        See engine1_tc.
    engine1_st : str or int, default=None
        Time limit in seconds for each move.
        If None, it is assumed that engine1_tc or engine1_npm is provided.
    engine2_st : str or TimeControl object, default=None
        See engine1_tc.
    engine1_npm : str or int, default=None
        Number of nodes per move the engine is allowed to search.
        If None, it is assumed that engine1_tc or engine1_st is provided.
    engine2_npm : str or int, default=None
        See engine1_npm.
    engine1_ponder : bool, default=False
        If True, allow engine1 to ponder.
    engine2_ponder : bool, default=False
        See engine1_ponder.
    timemargin : str or int, default=None
        Allowed number of milliseconds the engines are allowed to go over the time
        limit. If None, the margin is 0.
    opening_file : str, default=None
        Path to the file containing the openings. Can be .epd or .pgn.
        Make sure that the file explicitly has the .epd or .pgn suffix, as it
        is used to detect the format.
    adjudicate_draws : bool, default=False
        Specify, if cutechess-cli is allowed to adjudicate draws, if the
        scores of both engines drop below draw_score for draw_movecount number
        of moves. Only kicks in after draw_movenumber moves have been played.
    draw_movenumber : int, default=1
        Number of moves to play after the opening, before draw adjudication is
        allowed.
    draw_movecount : int, default=10
        Number of moves below the threshold draw_score, without captures and
        pawn moves, before the game is adjudicated as draw.
    draw_score : int, default=8
        Score threshold of the engines in centipawns. If the score of both
        engines drops below this value for draw_movecount consecutive moves,
        and there are no captures and pawn moves, the game is adjudicated as
        draw.
    adjudicate_resign : bool, default=False
        Specify, if cutechess-cli is allowed to adjudicate wins/losses based on
        the engine scores. If one engine’s score drops below -resign_score for
        resign_movecount many moves, the game is considered a loss for this
        engine.
    resign_movecount : int, default=3
        Number of consecutive moves one engine has to output a score below
        the resign_score threshold for the game to be considered a loss for this
        engine.
    resign_score : int, default=550
        Resign score threshold in centipawns. The score of the engine has to
        stay below -resign_score for at least resign_movecount moves for it to
        be adjudicated as a loss.
    adjudicate_tb : bool, default=False
        Allow cutechess-cli to adjudicate games based on Syzygy tablebases.
        If true, tb_path has to be set.
    tb_path : str, default=None
        Path to the folder containing the Syzygy tablebases.
    concurrency : int, default=1
        Number of games to run in parallel. Be careful when running time control
        games, since the engines can negatively impact each other when running
        in parallel.
    debug_mode : bool, default=False
        If True, pass ``-debug`` to cutechess-cli.

    Yields
    -------
    out : str
        Results of the cutechess-cli match streamed as str.
    """
    string_array = ["cutechess-cli"]
    string_array.extend(("-concurrency", str(concurrency)))

    if (engine1_npm is None and engine1_tc is None and engine1_st is None) or (
        engine2_npm is None and engine2_tc is None and engine2_st is None
    ):
        raise ValueError("A valid time control or nodes configuration is required.")
    string_array.extend(
        _construct_engine_conf(
            id=1,
            engine_npm=engine1_npm,
            engine_tc=engine1_tc,
            engine_st=engine1_st,
            engine_ponder=engine1_ponder,
            timemargin=timemargin,
        )
    )
    string_array.extend(
        _construct_engine_conf(
            id=2,
            engine_npm=engine2_npm,
            engine_tc=engine2_tc,
            engine_st=engine2_st,
            engine_ponder=engine2_ponder,
            timemargin=timemargin,
        )
    )

    if opening_file is None:
        raise ValueError("Providing an opening file is required.")
    opening_path = pathlib.Path(opening_file)
    if not opening_path.exists():
        raise FileNotFoundError(
            f"Opening file the following path was not found: {opening_path}"
        )
    opening_format = opening_path.suffix
    if opening_format not in {".epd", ".pgn"}:
        raise ValueError(
            "Unable to determine opening format. "
            "Make sure to add .epd or .pgn to your filename."
        )
    string_array.extend(
        (
            "-openings",
            f"file={str(opening_path)}",
            f"format={opening_format[1:]}",
            "order=random",
        )
    )

    if adjudicate_draws:
        string_array.extend(
            (
                "-draw",
                f"movenumber={draw_movenumber}",
                f"movecount={draw_movecount}",
                f"score={draw_score}",
            )
        )
    if adjudicate_resign:
        string_array.extend(
            ("-resign", f"movecount={resign_movecount}", f"score={resign_score}")
        )
    if adjudicate_tb:
        if tb_path is None:
            raise ValueError("No path to tablebases provided.")
        tb_path_object = pathlib.Path(tb_path)
        if not tb_path_object.exists():
            raise FileNotFoundError(
                f"No folder found at the following path: {str(tb_path_object)}"
            )
        string_array.extend(("-tb", str(tb_path_object)))

    string_array.extend(("-rounds", f"{rounds}"))
    string_array.extend(("-games", "2"))
    string_array.append("-repeat")
    string_array.append("-recover")
    if debug_mode:
        string_array.append("-debug")
    string_array.extend(("-pgnout", "out.pgn"))

    with subprocess.Popen(
        string_array, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    ) as popen:
        for line in iter(popen.stdout.readline, ""):
            yield line


def reduce_ranges(X, y, noise, space):
    X_new = []
    y_new = []
    noise_new = []
    reduction_needed = False
    for row, yval, nval in zip(X, y, noise):
        include_row = True
        for dim, value in zip(space.dimensions, row):
            if isinstance(dim, Integer) or isinstance(dim, Real):
                lb, ub = dim.bounds
                if value < lb or value > ub:
                    include_row = False
            elif isinstance(dim, Categorical):
                if value not in dim.bounds:
                    include_row = False
            else:
                raise ValueError(f"Parameter type {type(dim)} unknown.")
        if include_row:
            X_new.append(row)
            y_new.append(yval)
            noise_new.append(nval)
        else:
            reduction_needed = True
    return reduction_needed, X_new, y_new, noise_new
