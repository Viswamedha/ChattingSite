cd chat/migrations
del /f /Q *.*
@echo off
echo.>__init__.py
cd ../../
cd main/migrations
del /f /Q *.*
@echo off
echo.>__init__.py
cd ../../
psql -c "DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;" -c "\q" "host=127.0.0.1 port=5432 user=postgres password=goosebumps dbname=chattingsite" 
python manage.py makemigrations
python manage.py migrate