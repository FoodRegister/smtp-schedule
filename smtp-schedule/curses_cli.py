

import curses
from curses import wrapper

EXPOSED_WRITE_MAIL = None

def main(stdscr):
    stdscr.clear()
    maxy, maxx = stdscr.getmaxyx()
    #stdscr.addstr(0, 0, "".join([" " for i in range(maxx)]), curses.A_STANDOUT)
    #stdscr.refresh()

    def write_mail(mails):
        for idx in range(3, maxy - 2):
            stdscr.addstr(idx, 1, "")
            stdscr.clrtoeol()
        
        if len(mails) == 0:
            stdscr.addstr(1, 1, "ID    FROM    TO    SUBJECT", curses.A_BOLD)
            stdscr.clrtoeol()
            stdscr.refresh()
            return

        maximal_mail = max(2, len(str(len(mails))), len(str(maxy - 3))) + 4
        maximal_from = max(4, *map(lambda x: len(x.mail_from), mails)) + 4 + maximal_mail
        maximal_to = max(
            2,
            *map(lambda mail: len(", ".join(mail.rcpt_tos)), mails)
        ) + 4 + maximal_from
        stdscr.addstr(1, 1, "ID", curses.A_BOLD)
        stdscr.clrtoeol()
        stdscr.addstr(1, maximal_mail, "FROM", curses.A_BOLD)
        stdscr.addstr(1, maximal_from, "TO", curses.A_BOLD)
        stdscr.addstr(1, maximal_to, "SUBJECT", curses.A_BOLD)
        for idx, mail in zip(range(3, maxy - 2), mails):
            stdscr.addstr(idx, 1, str(idx - 2))
            stdscr.clrtoeol()

            stdscr.addstr(idx, maximal_mail, mail.mail_from)
            stdscr.addstr(idx, maximal_from, ", ".join(mail.rcpt_tos))

            for ln in mail.content.decode('utf8', errors='replace').splitlines():
                if 'Subject: ' == ln[:9]:
                    stdscr.addstr(idx, maximal_to, ln[9:])
                    break
        stdscr.refresh()

    global EXPOSED_WRITE_MAIL
    EXPOSED_WRITE_MAIL = write_mail

    string = ""
    while True:
        while CHARACTER := stdscr.getch():
            if chr(CHARACTER) == '\n': break

            if CHARACTER != 127:
                string += chr(CHARACTER)
            else:
                string = string[:-1]
            
            stdscr.addnstr(maxy-1, 0, string, maxx-1)
            stdscr.clrtoeol()
            stdscr.refresh()
            if CHARACTER == "": return
        
        if string == ":q": break

        string = ""
        stdscr.addnstr(maxy-1, 0, string, maxx-1)
        stdscr.clrtoeol()
        stdscr.refresh()
    pass

def run():
    wrapper(main)
