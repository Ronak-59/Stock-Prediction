<?php
define("DBHOST","localhost");
define("DBUSER", "root");
define("DBPWD", "");
define("DB", "user_data");
$date = date_default_timezone_set('Asia/Kolkata');
error_reporting(E_ALL ^ E_DEPRECATED);
$conn = mysqli_connect(DBHOST,DBUSER,DBPWD,DB);
if(mysqli_connect_errno())
{
	echo mysqli_connect_errno();
	die("Connection failed: " . mysqli_connect_error());
}

$stock=array("MMM","AXP","AAPL","BA","CAT","CVX","CSCO","KO","DIS","DWDP","XOM","GE","GS","HD","IBM",
	"INTC","JNJ","JPM","MCD","MRK","MSFT","NKE","PFE","PG","TRV","UTX","UNH","VZ","V","WMT");

$data1="SELECT * FROM users;";
$result= @mysqli_query($conn,$data1);
$data;
$pred =[10.0, 6.36, 6.62, 6.81, 8.9, 3.35, 4.67, 6.91, 2.16, 6.55, 3.92, 4.72, 7.29, 3.34, 6.58, 2.56, 3.52, 3.99, 2.29, 6.73, 5.98, 4.85, 3.49, 2.65, 4.96, 5.06, 6.2, 1.07, 0.0, 1.8];
while($row = @mysqli_fetch_assoc($result))
{
	$data[] = $row;
}

$datafin[] = 0;
$userquant;
$a = array_fill(0,30,0);
$b = array_fill(0,30,0);
//for($j=1;$j<=10;$j++)
//{
	$j=0;
	
		$data2="SELECT * FROM users where  transaction_type='BUY' and user_id=4;";
		$datainf="SELECT * FROM users where  transaction_type='SELL' and user_id=4;";
		$result= @mysqli_query($conn,$data2);
		$resultinf= @mysqli_query($conn,$datainf);
		while($row = @mysqli_fetch_assoc($result))
		{
			
			$stktype = $row['symbol'];
			//$stktype = array_search($stktype,$stock);
			for($j=0;$j<=29;$j++){
				if($stock[$j]==$stktype)
					break;
			}
			
			$c = $a[$j];
			//print_r($a[$j]);
			$c+=(float)$row['amount'];
			$a[$j]=$c;
			$c = $b[$j];
			$c+=(float)$row['quantity'];
			$b[$j]=$c;
			//print_r($a);
		}
		while($row = @mysqli_fetch_assoc($resultinf))
		{
			
			$stktype = $row['symbol'];
			//$stktype = array_search($stktype,$stock);
			for($j=0;$j<=29;$j++){
				if($stock[$j]==$stktype)
					break;
			}
			
			$c = $a[$j];
			//print_r($a[$j]);
			$c-=(float)$row['amount'];
			$a[$j]=$c;
			$c = $b[$j];
			$c-=(float)$row['quantity'];
			if($c>0)
				$b[$j]=$c;
			else
				$b=0;
			//print_r($a);
		}
		
		for($j=0;$j<=29;$j++){
				if($a[$j]!=0){
					$f="https://api.intrinio.com/data_point?ticker=".$stock[$j]."&item=last_price";
				$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => $f,
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => array(
    "Authorization: Basic ZTYzMWRhOTU4ZTIwYWEyOWJkMTYzOGFhYTg0NDAwNDg6Y2EyZjcxNzU3ZTY2MGZkYTE5ZjQ2M2FlMzg0YTg3NTQ=",
    "Cache-Control: no-cache",
    "Postman-Token: 1b6ff9c1-2a1f-aa54-a8d1-4adc6fef419f"
  ),
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  $json = json_decode($response,true);
  //echo $json['value'];
}	
				if($b[$j]!=0)	
					$a[$j]=$a[$j]/$b[$j];
				
				$a[$j]=$json['value']-$a[$j];
				if($pred[$j]>5)
					$a[$j]=0;
				else
					$a[$j]=$a[$j]*$pred[$j];
					//print_r($stock[$j]);
				//print_r($a[$j]);
				}
				
		}
		
		$w=array();
		$x=array();
		
		$e=0;
		$min=0;
		//print_r($x);
		$comb = array_combine($stock, $a);
		asort($comb);	
		print_r($comb);	
		
		//print_r($w);


?>