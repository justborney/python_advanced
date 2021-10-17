import time


def main():
    print('Start program and going to sleep')
    time.sleep(2)
    user_input = input()
    print(f'User name: {user_input}')
    user_input = input()
    print(f'User surname: {user_input}')
    user_input = input()
    print(f'User age: {user_input}')
    print('Done sleeping 2 seconds. Bye!')


if __name__ == '__main__':
    main()
