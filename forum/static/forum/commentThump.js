$(document).ready(
    function thumpUpComment(){
        $('.comment_thump_up').click(function(e){
            console.log('click');
            e.preventDefault();
            var $this = $(this);
            // get the sibling(thump up and down count) of the thump up id
            var $thumpUpCount = $this.siblings('#comment_thump_up_count');
            var parsedUpCount = parseInt($thumpUpCount.text());
            var $thumpDownCount = $this.siblings('#comment_thump_down_count');
            var parsedDownCount = parseInt($thumpDownCount.text());
            var url = $this.attr('comment_up_url');

            
            // ajax call
            $.ajax({
                type: 'get',
                url: url,
                success: function(data){
                    if (data.added){
                        $thumpUpCount.text(parsedUpCount += 1);
                        if (data.already_thumped_down && parsedDownCount >= 0){
                            $thumpDownCount.text(parsedDownCount -= 1);
                        }
                    }else{
                        $thumpUpCount.text(parsedUpCount -= 1);
                    }
                },
                error: function(response){
                    /// the logic will be in the frontend

                }
            });
        });
    }
)


$(document).ready(
    function thumpDownComment(){
        $('#comment_thump_down').click(function(e){
            e.preventDefault();
            var $this = $(this);
            // get the sibling(thump up and down count) of the thump up id
            var $thumpDownCount = $this.siblings('#comment_thump_down_count');
            var parsedDownCount = parseInt($thumpDownCount.text());
            var $thumpUpCount = $this.siblings('#comment_thump_up_count');
            var parsedUpCount = parseInt($thumpUpCount.text())
            var url = $this.attr('comment_down_url');

            
            // ajax call
            $.ajax({
                type: 'get',
                url: url,
                success: function(data){
                    if (data.added){
                        $thumpDownCount.text(parsedDownCount + 1);
                        if (data.already_thumped_up && parsedUpCount > 0){
                            $thumpUpCount.text(parsedUpCount - 1);
                        }
                    }else{
                        $thumpDownCount.text(parsedDownCount - 1);
                    }
                },
                error: function(response){
                    /// the logic will be in the frontend

                }
            });
        });
    }
)