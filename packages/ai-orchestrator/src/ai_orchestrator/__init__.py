import anyio


from ai_orchestrator.app import start


def main():
    try:
        anyio.run(start)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
