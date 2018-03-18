<?php
	// array for JSON response
	$conn = mysqli_connect('localhost','root','','user_data');
			echo "<form action='getdetails.php' method='POST'><input type='text' name='userid'></input>
			<input type='submit'></input></form>";
			$userid = $_POST['userid'];
			$decoded_data = json_decode(exec('python ml.py'), true);
			echo $decoded_data['0'];
			//open database connection
			$qry1="SELECT * FROM users where user_id = $userid";
			$result2 = mysqli_query($conn,$qry1);
			$arr = array();
			while($row = mysqli_fetch_assoc($result2))
			{
				array_push($arr, $row['uid']);
			}
			$x = max($arr);
			$qry2 = "SELECT demat from users where uid = $x";
			$result1 = mysqli_query($conn,$qry2);
			while($row = mysqli_fetch_assoc($result1))
			{
				$demat = $row['demat'];
			}
			echo "Demat = ".$demat."\n";
			$stocksarr = array();
			$i = 0;
			$filenames = array('AAPL','AXP','BA','CAT','CSCO','CVX','DIS','DWDP','GE','GS','HD','IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','TRV','UNH','UTX','V','VZ','WMT','XOM');
			for($i = 0; $i < sizeof($filenames); $i++)
			{ 
				$st = $filenames[$i];
				$stockarray = "SELECT * from users where user_id = $userid and symbol = '$st'";
				$resultstock = mysqli_query($conn,$stockarray);
				$stocktotal = 0;
				$arry = array();
				if(mysqli_num_rows($resultstock)>0)
				{
					while($row = mysqli_fetch_assoc($resultstock))
					{
						if($row['transaction_type'] == 'BUY')
						{
							$stocktotal = $stocktotal + $row['amount'];
						}
						else if($row['transaction_type'] == 'SELL')
						{
							$stocktotal = $stocktotal - $row['amount'];
						}
					}
					array_push($stocksarr, $stocktotal);
				}
				else
				{
					array_push($stocksarr, 0);
				}
			}
			for($i = 0; $i < sizeof($filenames); $i++)
			{
				echo $stocksarr[$i]."\n";
			}
			$data = '{"dmatbal": $demat, "weights": $stocksarr}';
			$result = shell_exec('python C:\Users\dell\PycharmProjects\house\ml.py' . escapeshellarg(json_encode($data)));
			$resultData = json_decode($result, true);
			var_dump($resultData);
	
?>