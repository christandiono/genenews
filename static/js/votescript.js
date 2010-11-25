$(document).ready(function(){
    $("img.vote").click(function(){
        var temp = this.id.split("_")
        $.ajax({type:"POST",
            url: "/article/vote/",
            data: {"direction": temp[0], "article_id": temp[1]},
            success: function(data){
                    if (data.changed_other){
                        if (data.direction == 'up'){
                            $('img.vote#down_'+data.id).attr('src', '/images/adowngray.gif');
                        } else {
                            $('img.vote#up_'+data.id).attr('src', '/images/aupgray.gif');
                        }
                    }
                    $('img.vote#'+data.direction+'_'+data.id).attr('src', '/images/a'+data.direction+data.color_this+'.gif');
                },
            dataType: "json"
            });
        });
    });
