echo "Ensure SPI is on"
sudo dtparam spi=on
# echo "Create cronjob"
# echo "* * * * * /home/pi/e_paper_weather_display/weather.py >> /home/pi/e_paper_weather_display/weather_app.log 2>&1" >> crontab
echo "Set Script permissions"
chmod u+x weather.py