BASEDIR=$(find $HOME/coding -type d  -name injae | head -1)

echo "Testing.."
mypy $BASEDIR/main.py
if [ $? -eq 0 ]
then
    echo "Test is Ok"
    python main.py
else
    echo "이건 분명 인재 탓이야.."
fi
