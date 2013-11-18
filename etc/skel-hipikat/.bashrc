###
# .bashrc - Adam Wright <adam@hipikat.org>
###

# Do nothing if not running interactively
[ -z "$PS1" ] && return


# $PATH (in increasing precedence)
declare -a paths=()

paths+=( /usr/games )
paths+=( /Developer/Tools )
paths+=( /usr/local/mysql/bin )
paths+=( /Applications/Xcode.app/Contents/Developer/usr/bin )
paths+=( /usr/local/sbin )
paths+=( /usr/local/bin )
#paths+=( /usr/local/share/python )
#paths+=( /usr/local/share/python )
paths+=( ~/.bin ~/bin ~/Dropbox/bin )

#paths+=( /opt/node /opt/node/lib/node_modules /opt/node/bin )

#TMP=:$PATH:
#REMOVE=:/usr/local/bin:
#TMP=${TMP/$REMOVE/:}
#TMP=${TMP%:}
#TMP=${TMP#:}

for (( i=0; i<${#paths[@]}; i++ )); do
    if [ -d ${paths[i]} ]; then
        #if [[ $PATH != *${paths[i]}* ]]; then
            PATH="${paths[i]}:${PATH}"
        #fi
    fi
done

# OH WHAT THE HELL
PATH=$PATH:.

# Python path setup
#export PYTHONPATH="$HOME/lib/python:."

# ALIASES (AND FUNCTIONS ACTING AS ALIASES)
alias lv='ls -l'            # List visible, vertical & verbose
alias la='ls -Al'           # List all, with details
alias scr='screen -D -R'    # Attach here and now
alias myip="curl -s icanhazip.com"

sassy()
{
    cd "src/styles"
    eval "bundle exec compass watch &"
    cd "../.."
}
runs() {
    eval "django-admin.py runserver 8890 --traceback"
}
runsp() {
    eval "django-admin.py runserver 8890 --traceback"
}
dev() {
    sassy
    runs
}
devp() {
    sassy
    runsp
}

function lvl() { ls $COLOR_ALWAYS -l "$@" | less ;}
function lal() { ls $COLOR_ALWAYS -Al "$@" | less ;}
function grepl() { grep $COLOR_ALWAYS "$@" | less ;}

# .bash_aliases
if [ -f .bash_aliases ]; then
    source .bash_aliases
fi

# Common typos
alias al='la'
alias vl='lv'
alias tial='tail'
alias poing='ping'
alias pign='ping'

# Common servers
alias dewclaw='ssh hipikat.org'

# ENVIRONMENT VARIABLES
export PAGER='less'
export EDITOR='vim'
export VISUAL="${EDITOR}"
export FCEDIT="${EDITOR}"
export CVSEDITOR="${EDITOR}"

export COPYFILE_DISABLE=true        # Stop problems with ghost ._ files on OS X
export LESS="-iR"                   # Ignore case when pattern is all lowercase & print raw control characters
export HISTCONTROL=ignoredups       # Ignore duplicate history entries
export TAR_OPTIONS="--exclude *.DS_Store*"

#export DYLD_LIBRARY_PATH=/usr/lib/instantclient_10_2


# PROGRAMMABLE COMPLETION
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    source /etc/bash_completion
fi


# SHELL OPTIONS
shopt -s checkwinsize               # Check the window size after each command and update LINES and COLUMNS
shopt -s cdspell                    # Correct minor directory spelling mistakes for cd
shopt -s cmdhist                    # Save multi-line commands to the history as a single line
shopt -s dotglob                    # Includes hidden files in pathname expansion
shopt -s extglob                    # Enables [?*+@!](pattern|pattern|...) matching
shopt -s nocaseglob                 # Pathname expansion matches in a case-insensitive way
shopt -s histappend                 # Append to the history file instead of overwriting it
shopt -s extdebug > /dev/null 2>&1  # Enable behavior intended for use by debuggers (for trap 'pre_execute' DEBUG)
shopt -s autocd                     # Change to a directory if a directory's given as a command


# COMMAND OPTIONS
# Make less more friendly for various files
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# Enable color support in various commands
if [ "$TERM" != "dumb" ]; then
    if [ -x /usr/bin/dircolors ]; then
        test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
        for cmd in ls dir vdir grep fgrep egrep
        do
            alias $cmd="$cmd --color=auto"
        done
        export COLOR_ALWAYS="--color=always"
    else
        export CLICOLOR_FORCE='TRUE'        # Probably on a Mac
        alias ls='ls -G -F'
    fi
fi


# UTILITY FUNCTIONS
function set_xterm_title () {
    echo -ne "\033]0;$1\007"
}

function set_screen_title () {
    if [[ $TERM == screen ]]; then
        echo -ne "\033k$1\033\\"
    fi
}

function set_env_variables() {
    # Replace home directories in $PWD with a ~
    local pwd_short=`echo -n $PWD | sed -e "s:\(^$HOME\):~:" | sed -e "s:\(^/home/\):~:" | sed -e "s:\(^/Users/\):~:"`
    # Truncate all but first and last three directories
    pwd_short=`echo -n $pwd_short | sed -e "s|^\(\~\?/[^/]*/[^/]*/[^/]*/\)[^/]*/.*\(/[^/]*/[^/]*/[^/]*/\?\)$|\1···\2|"`
    # Truncate any directories longer than 18 character down to 15
    pwd_short=`echo -n $pwd_short | sed -e "s|/\([^/]\{15\}\)\([^/]\{3\}\)[^/]\+|/\1···|g"`
    PWD_SHORT=$pwd_short
    unset pwd_short

    if [[ $EUID -ne 0 ]]; then
        PROMPT_COLOUR=`echo -ne "1;37m"`  # White
    else
        PROMPT_COLOUR=`echo -ne "1;31m"`  # Red
    fi

    if [[ -n $WINDOW ]]; then
        WINDOW_NUMBER="$WINDOW) "
    else
        WINDOW_NUMBER=""
    fi

    VCS_BRANCH=`git branch --no-color 2> /dev/null | grep -e '\* ' | sed 's/^..\(.*\)/ \*\1/'`
}


# PROMPTS AND WINDOW TITLES
PS1='\[\033[1;32m\]${WINDOW_NUMBER}\[\033[0;32m\]\u@${HOST_ALIAS:-\h}\[\033[0m\]:\[\033[0;34m\]$PWD_SHORT\[\033[0;36m\]$VCS_BRANCH \[\033[${PROMPT_COLOUR}\]# \[\033[m\]'
PS2='\[\033[01;32m\] >\[\033[0;37m\] '
bash_interactive_mode=""

function pre_prompt() {
    set_env_variables
    set_xterm_title "$USER@$HOST_ALIAS"
    set_screen_title "$HOST_ALIAS $PWD_SHORT #"

    bash_interactive_mode="yes"
}
PROMPT_COMMAND=pre_prompt       # Installs pre_prompt to run before the prompt is displayed

# Executed before each command; returns early if not being run interactively
function pre_execute() {
    if [[ -n "$COMP_LINE" ]]; then
        # We're inside a completer so we can't be running interactively
        return
    fi
    if [[ -z "$bash_interactive_mode" ]]; then
        # Doing something related to displaying the prompt; let the prompt set the tile
        return
    else
        if [[ 0 -eq "$BASH_SUBSHELL" ]]; then
            # If in a subshell, the prompt won't be re-displayed to put us back in interactive mode
            bash_interactive_mode=""
        fi
    fi
    if [[ "$BASH_COMMAND" == "pre_prompt" ]]; then
        # Consecutive prompts; switch out of interactive and don't trace commands in pre_prompt
        bash_interactive_mode=""
        return
    fi

    # If we get this far, the command should be interactive
    # We use history instead of BASH_COMMAND so we can get a full command including pipes
    set_env_variables
    local this_command=`history 1 | sed -e "s/^[ ]*[0-9]*[ ]*//g"`;

    set_screen_title "$HOST_ALIAS $PWD_SHORT \$ $this_command"

    # Return the terminal to its default colour; the prompt may have changed it
    echo -en "\033[00m"
}
trap 'pre_execute' DEBUG

# Django bash completion
if [ -f ~/.django_bash_completion.sh ]; then
    source ~/.django_bash_completion.sh
fi

# LOCAL COMMANDS
if [ -f ~/.bash_local ]; then
    source ~/.bash_local
fi


PATH=$PATH:$HOME/.rvm/bin # Add RVM to PATH for scripting
[[ -r $rvm_path/scripts/completion ]] && . $rvm_path/scripts/completion


