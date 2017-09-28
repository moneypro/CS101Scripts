for filename in "$@"
do
	LANG=C sed -i 's/[\d128-\d255]//g' $filename
done
