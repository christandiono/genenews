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

                    var new_color;
                    if (data.color_this == 'mod'){
                        if (data.direction == 'up' ){
                            new_color = 'red';
                        } else {
                            new_color = 'blue';
                        }
                    } else {
                        new_color = '';
                    }

                    var points = parseInt($('span#points_' +data.id).text());
                    
                    if (data.changed_other) {
                        if (data.direction == 'up'){
                            points = points + 2;
                        } else {
                            points = points - 2;
                        }
                    } else {
                        if (new_color == 'red') {
                            points = points + 1;
                        } else if (new_color == 'blue') {
                            points = points - 1;
                        } else if (new_color == '') {
                            if (data.direction == 'up') {
                                points = points - 1;
                            } else {
                                points = points + 1;
                            }
                        }
                    }

                    $('span#points_'+data.id).replaceWith('<span class="'+new_color+'" id="points_'+data.id+'">'+points+'</span>');



                    
                },
            dataType: "json"
            });
        });
    });
