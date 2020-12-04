# injae dir
BASEDIR=$(find $HOME/coding -type d  -name injae | head -1)
STUBDIR=$(find $BASEDIR -type d  -name stubs | head -1)

export MYPYPATH=$STUBDIR

mypy $STUBDIR
if [ $? -eq 0 ]
then
    echo "Test is Ok"
    python main.py
else
    echo "이건 분명 인재 탓이야.."
fi
