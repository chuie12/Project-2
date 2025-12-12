from logic import *

def main():
    """Main function that calls login window followed by the account window upon successful login"""
    application = QApplication([])

    login = LoginDialog()
    if login.exec() == LoginDialog.DialogCode.Accepted:
        window = Logic()
        window.show()
        application.exec()

if __name__ == '__main__':
    main()