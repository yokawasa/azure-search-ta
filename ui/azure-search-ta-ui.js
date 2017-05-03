var inSearch = false;
var detailMode= false;

function execSearch()
{
	var text = $("#ta_text").val();
    var analyzer = $("#ta_analyzer").val();
    var index = $("#ta_index").val();
	var searchAPI1 = "/analyze-api.php";
	inSearch= true;

    var postdata = {
       "text": text,
       "analyzer": analyzer,
       "index": index
    };
    $.ajax({
        url: searchAPI1,
        beforeSend: function (request) {
            request.setRequestHeader("Accept", "application/json");
        },
        data: postdata,
        type: "POST",
        success: function (data) {

			$( "#apidata-container" ).html('');
    		$( "#apidata-container" ).append('<h2>Output Tokens</h2>');
			for (var item in data.tokens)
			{
                $( "#apidata-container" ).append( ' <kbd class=lead>' + data.tokens[item].token + '</kbd> ');
            }
			inSearch= false;
        }
    });

}

