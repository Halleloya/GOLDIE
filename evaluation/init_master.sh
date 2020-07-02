cd ../../
python -m IoT.level1.init_db --drop
python -m IoT.level3.init_db --drop
python -m IoT.level5.init_db --drop
python -m IoT.level5b.init_db --drop

python -m IoT.level1.run &
echo $!
python -m IoT.level3.run &
echo $!
python -m IoT.level5.run &
echo $!
python -m IoT.level5b.run &
echo $!

echo $$