ITIMER_PROF=2L
ITIMER_REAL=0L
ITIMER_VIRTUAL=1L
def ItimerError(*args, **kwargs): pass
NSIG=65
SIGABRT=6
SIGALRM=14
SIGBUS=7
SIGCHLD=17
SIGCLD=17
SIGCONT=18
SIGFPE=8
SIGHUP=1
SIGILL=4
SIGINT=2
SIGIO=29
SIGIOT=6
SIGKILL=9
SIGPIPE=13
SIGPOLL=29
SIGPROF=27
SIGPWR=30
SIGQUIT=3
SIGRTMAX=64
SIGRTMIN=34
SIGSEGV=11
SIGSTOP=19
SIGSYS=31
SIGTERM=15
SIGTRAP=5
SIGTSTP=20
SIGTTIN=21
SIGTTOU=22
SIGURG=23
SIGUSR1=10
SIGUSR2=12
SIGVTALRM=26
SIGWINCH=28
SIGXCPU=24
SIGXFSZ=25
SIG_DFL=0
SIG_IGN=1
__doc__='This module provides mechanisms to use signal handlers in Python.\n\nFunctions:\n\nalarm() -- cause SIGALRM after a specified time [Unix only]\nsetitimer() -- cause a signal (described below) after a specified\n               float time and the timer may restart then [Unix only]\ngetitimer() -- get current value of timer [Unix only]\nsignal() -- set the action for a given signal\ngetsignal() -- get the signal action for a given signal\npause() -- wait until a signal arrives [Unix only]\ndefault_int_handler() -- default SIGINT handler\n\nsignal constants:\nSIG_DFL -- used to refer to the system default handler\nSIG_IGN -- used to ignore the signal\nNSIG -- number of defined signals\nSIGINT, SIGTERM, etc. -- signal numbers\n\nitimer constants:\nITIMER_REAL -- decrements in real time, and delivers SIGALRM upon\n               expiration\nITIMER_VIRTUAL -- decrements only when the process is executing,\n               and delivers SIGVTALRM upon expiration\nITIMER_PROF -- decrements both when the process is executing and\n               when the system is executing on behalf of the process.\n               Coupled with ITIMER_VIRTUAL, this timer is usually\n               used to profile the time spent by the application\n               in user and kernel space. SIGPROF is delivered upon\n               expiration.\n\n\n*** IMPORTANT NOTICE ***\nA signal handler function is called with two arguments:\nthe first is the signal number, the second is the interrupted stack frame.'
__name__='signal'
__package__=None
def alarm(*args, **kwargs): pass
def default_int_handler(*args, **kwargs): pass
def getitimer(*args, **kwargs): pass
def getsignal(*args, **kwargs): pass
def pause(*args, **kwargs): pass
def set_wakeup_fd(*args, **kwargs): pass
def setitimer(*args, **kwargs): pass
def siginterrupt(*args, **kwargs): pass
def signal(*args, **kwargs): pass
