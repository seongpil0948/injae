# mypy main.py
$python = python -V

if[$python -eq 3.7.3]
then
    echo ok!
else
    echo Not ok!
echo $?
# if [$? -eq]