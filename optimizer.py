from gear_optimizer.gui import gui

if __name__ == '__main__':
    try:
        app = gui.Application()
        app.start_optimizer_with_gui()
    except Exception as e:
        print(e)
        input("Press Enter to continue...")
