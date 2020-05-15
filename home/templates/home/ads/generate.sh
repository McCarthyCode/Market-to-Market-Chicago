#!/bin/bash

leaderboard1=( 24 )
leaderboard2=(  )
large_mobile_banner1=( 24 )
large_mobile_banner2=(  )
medium_rectangle1=( 65 )
medium_rectangle2=( 66 )
medium_rectangle3=( 67 )
medium_rectangle4=( 68 )

for i in "${leaderboard1[@]}" ; do
    output=`printf 'leaderboard%02d.html' $i`
    printf '<a id="leaderboard1" href="javascript:void(0);">
  <img src="https://via.placeholder.com/728x90?text=Leaderboard+%d" alt="Leaderboard %d">
</a>\n' $i $i > $output
done

for i in "${leaderboard2[@]}" ; do
    output=`printf 'leaderboard%02d.html' $i`
    printf '<a id="leaderboard2" href="javascript:void(0);">
  <img src="https://via.placeholder.com/728x90?text=Leaderboard+%d" alt="Leaderboard %d">
</a>\n' $i $i > $output
done

for i in "${large_mobile_banner1[@]}" ; do
    output=`printf 'large_mobile_banner%02d.html' $i`
    printf '<a id="largeMobileBanner1" href="javascript:void(0);">
  <img src="https://via.placeholder.com/320x100?text=Large+Mobile+Banner+%s" alt="Large Mobile Banner %s">
</a>\n' $i $i > $output
done

for i in "${large_mobile_banner2[@]}" ; do
    output=`printf 'large_mobile_banner%02d.html' $i`
    printf '<a id="largeMobileBanner2" href="javascript:void(0);">
  <img src="https://via.placeholder.com/320x100?text=Large+Mobile+Banner+%s" alt="Large Mobile Banner %s">
</a>\n' $i $i > $output
done

for i in "${medium_rectangle1[@]}" ; do
    output=`printf 'medium_rectangle%02da.html' $i`
    printf '<a id="mediumRectangle1a" class="d-none d-md-block" href="javascript:void(0);">
  <img src="https://via.placeholder.com/300x250?text=Medium+Rectangle+%s" alt="Medium Rectangle %sa">
</a>\n' $i $i > $output
    output=`printf 'medium_rectangle%02db.html' $i`
    printf '<a id="mediumRectangle1b" class="d-block d-md-none" href="javascript:void(0);">
  <img src="https://via.placeholder.com/300x250?text=Medium+Rectangle+%s" alt="Medium Rectangle %sb">
</a>\n' $i $i > $output
done

for i in "${medium_rectangle2[@]}" ; do
    output=`printf 'medium_rectangle%02d.html' $i`
    printf '<a id="mediumRectangle2" class="d-block" href="javascript:void(0);">
  <img src="https://via.placeholder.com/300x250?text=Medium+Rectangle+%s" alt="Medium Rectangle %s">
</a>\n' $i $i > $output
done

for i in "${medium_rectangle3[@]}" ; do
    output=`printf 'medium_rectangle%02d.html' $i`
    printf '<a id="mediumRectangle3" class="d-block" href="javascript:void(0);">
  <img src="https://via.placeholder.com/300x250?text=Medium+Rectangle+%s" alt="Medium Rectangle %s">
</a>\n' $i $i > $output
done

for i in "${medium_rectangle4[@]}" ; do
    output=`printf 'medium_rectangle%02d.html' $i`
    printf '<a id="mediumRectangle4" class="d-block" href="javascript:void(0);">
  <img src="https://via.placeholder.com/300x250?text=Medium+Rectangle+%s" alt="Medium Rectangle %s">
</a>\n' $i $i > $output
done
