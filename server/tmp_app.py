from App import main_app
from OkatronState import Status

okatron = main_app()

def main():
    while True:
        # if start_processing:
        # try:
        okatron.server.state.status = Status.WORKING
        frame = okatron.server.run()

if __name__ == "__main__":
    main()