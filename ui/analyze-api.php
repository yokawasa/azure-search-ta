<?php

$azureSearchAccount="<Azure Search Service name>";
$azureSearchApiKey = "<Azure Search API Admin Key>";

$req=$_REQUEST;
$params = array();
if( is_array($req) ) {
    foreach( $req as $name => $value) {
        $params[$name] = $value;
    }
}
if ( !array_key_exists('text', $params) 
      || !array_key_exists('analyzer', $params) 
      || !array_key_exists('index', $params) ) {
    print "Error!";
    exit;
}

$AZURESEARCH_URL_BASE= 'https://'.$azureSearchAccount.'.search.windows.net/indexes/'.$params['index'].'/analyze?api-version=2015-02-28-Preview';

$body_arr = array(
    "text" => $params['text'],
    "analyzer" => $params['analyzer']
);

$header = array(
    "Content-Type: application/json; charset=UTF-8",
    "Api-Key: ". $azureSearchApiKey,
    "Accept': application/json",
    "Accept-Charset: UTF-8"
);
$context = array(
    "http" => array(
        "method"  => "POST",
        "header"  => implode("\r\n", $header),
        "content" => json_encode($body_arr)
    )
);

$res_data = file_get_contents($AZURESEARCH_URL_BASE, false, stream_context_create($context));

if ($res_data  === false) {
    print "Error!";
}
else
{
    header('Content-Length: '.strlen($res_data));
    header('Content-Type: application/json; odata.metadata=minimal');
    header('Access-Control-Allow-Origin: *');
    print $res_data;
}

?>
