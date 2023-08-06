from subprocess import run


def play():
    args = [
        "gunicorn",
        "--worker-class",
        "eventlet",
        "-w",
        "1",
        'game_theory_optimal_poker:create_app()',
    ]
    run(args)


if __name__ == "__main__":
    play()
