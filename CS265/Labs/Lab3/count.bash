
for item in $( ls )
do

	if $( test -f $item )
	then
		word_count=$( wc -w < $item)
		line_count=$( wc -l < $item)
		echo $item $line_count $word_count
	fi

done











