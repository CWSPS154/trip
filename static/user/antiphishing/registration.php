<?php

include("connection.php");
include('functions.php');

$response=array();
$name=$_POST['name'];
$ph=$_POST['phone_no'];
$hn=$_POST['house_name'];
$dis=$_POST['district'];
$pin=$_POST['pin'];
$gen=$_POST['gender'];
$eid=$_POST['email_id'];
$ano=$_POST['acc_no'];
$pw=$_POST['password'];

$share=$_FILES['file']['name'];
move_uploaded_file($_FILES['file']['tmp_name'],"share/a.jpg");

$image=$_FILES['pfile']['name'];
move_uploaded_file($_FILES['pfile']['tmp_name'],"../user_pic/".$image);

$a=mysql_query("insert into login values(null,'$eid','$pw','pending')");
$lid=mysql_insert_id();

$res=mysql_query("insert into user(user_id,name,ph_no,house_name,district,pin,gender,email_id,acc_no,profile_pic)values('$lid','$name','$hn','$hn','$dis','$pin','$gen','$eid','$ano','$image')");

// if(1==1)
if($res>0)
{
//text to hidden-----------
// $message_to_hide = "qwe";
// $eid="riss.kiran@gmail.com";
// $lid="87";
$message_to_hide = $pw;
$binary_message = toBin($message_to_hide);
$message_length = strlen($binary_message);

//======================================================================================
// image file 
$src = "C:\wamp\www\antiphishing\AndroidConnections\share\a.jpg";
$im = imagecreatefromjpeg($src);

for($x=0;$x<$message_length;$x++){
  $y = $x;
  $rgb = imagecolorat($im,$x,$y);
  $r = ($rgb >>16) & 0xFF;
  $g = ($rgb >>8) & 0xFF;
  $b = $rgb & 0xFF;
  
  $newR = $r;
  $newG = $g;
  $newB = toBin($b);
  $newB[strlen($newB)-1] = $binary_message[$x];
  $newB = toString($newB);
  
  $new_color = imagecolorallocate($im,$newR,$newG,$newB);
  imagesetpixel($im,$x,$y,$new_color);
}

imagepng($im,"share/simple.jpg");
imagedestroy($im);

//======================================================================================
        $image = file_get_contents("share/simple.jpg");
        
        $cipher = "aes-128-cbc";
        $ivlen = openssl_cipher_iv_length($cipher);

        //----------------------------------------------
        $iv = openssl_random_pseudo_bytes($ivlen);
        $key = openssl_random_pseudo_bytes(128);
		
		$eiv=base64_encode($iv);
		$ekey=base64_encode($key);
		
        //-------------------------------------------------------------------------

        $ciphertext = openssl_encrypt($image, $cipher, $key, $options=0, $iv);
        $encd=base64_encode($ciphertext);

//-----------------------------------------------------
        $sp=strlen($encd)/2;
        if(strlen($encd)%2>0){
          $sp=$sp+1;
        }

        $first400 = substr($encd, 0, $sp);
        $theRest = substr($encd, $sp);

        file_put_contents("share/".$lid."_shr1.jpg", $first400);
        file_put_contents("share/".$lid."_shr2.jpg", $theRest);
	
//-----------------------------------------------------	
		//send share1 to mail		
		$re=mysql_query("SELECT * FROM skeys WHERE `sid`='$lid'");
		if(mysql_num_rows($re)>0)
		{	
			mysql_query("update `skeys` SET `iv`='$eiv',`skey`='$ekey' WHERE `sid`='$lid'");
		}
		else{
			$a=mysql_query("INSERT INTO `skeys` VALUES('$lid','$eiv','$ekey')");
		}

// //-------------------------------------------------------------------------------------------
// //-------------------------------------------------------------------------------------------

// 		$qr="SELECT * FROM skeys WHERE `sid`='$lid'";
//     	echo $qr."<br>";
// 		$re=mysql_query($qr);
// 		if(mysql_num_rows($re)>0)
// 		{		
//         echo "hiiiiiii--------"."<br>";
//         $res=mysql_fetch_array($re);
//         echo "------------".$res["sid"]."<br>";
//         echo $res["iv"]."<br>";
//         echo $res["skey"]."<br>";

// 		$ssiv = base64_decode($res["iv"]);
//         $sskey = base64_decode($res["skey"]);
//         //----------------------------------------------
        
//         echo$iv.";;;;;;;;;;;;;<br>";
		
// 		$share1="share/".$lid."_shr1.jpg";
//     	$share2="share/".$lid."_shr2.jpg";
// 		$im1 = file_get_contents($share1);
//         $im2 = file_get_contents($share2);
//         echo $im1."*****--------"."<br>";

//         // $dcd=base64_decode($first400.$theRest);
//         $dcd=base64_decode($im1.$im2);

//         echo "==========--------"."<br>";
//         //decrpyt and display
//         // $img = openssl_decrypt($dcd, $cipher, $key, $options=0, $iv);
//         $img = openssl_decrypt($dcd, $cipher, $sskey, $options=0, $ssiv);
//         file_put_contents("bbbbbbbb.jpg", $img);
// //-------------------------------------------------
// //extract password

// 	$src = 'C:\wamp\www\antiphishing\AndroidConnections\bbbbbbbb.jpg';
// 	$im = imagecreatefrompng($src);
//         echo "111111111111111--------"."<br>";

// 	$real_message = '';

// 	for($x=0;$x<40;$x++){
//   		$y = $x;
//   		$rgb = imagecolorat($im,$x,$y);
//   		$r = ($rgb >>16) & 0xFF;
//   		$g = ($rgb >>8) & 0xFF;
//   		$b = $rgb & 0xFF;
  
//   		$blue = toBin($b);
//   		$real_message .= $blue[strlen($blue)-1];
// 	}
// 	$real_message = toString($real_message);
//   	echo "00000000000000000--------"."<br>";
//   	echo $real_message;

// 	}
// //-------------------------------------------------------------------------------------------

	// mail send start---------------------------
	try{	
		require("class.phpmailer.php");
		$mail = new PHPMailer(); // create a new object
		$mail->IsSMTP(); // enable SMTP
		$mail->SMTPDebug = 1; // debugging: 1 = errors and messages, 2 = messages only
		$mail->SMTPAuth = true; // authentication enabled
		$mail->SMTPSecure = 'tls'; // secure transfer enabled REQUIRED for GMail
		$mail->Host = "smtp.gmail.com";
		$mail->Port = 587;
		$mail->Username = "rosh@gmail.com";  // SMTP username gmail username
		$mail->Password = "roshpwd"; // SMTP password   gmail password
		
		$mail->From = "Antiphishing"; // from email address
		$mail->FromName = "Antiphishing"; //from name
		 
		$mail->AddAddress($eid);      
		$mail->AddAttachment("share/".$lid."_shr1.jpg");    
		$mail->IsHTML(true);                               
		
		$mail->Subject = "Registration Success";
		$mail->Body    = "Please save your share";
		$mail->AltBody = "";
		
		if(!$mail->Send())
		{
			$response["status"]="0";
		}
		else
		{
			$response["status"]="1";
		}
	}catch (Exception $e)
		
	{
		$response["status"]="0";
	}	
	///mail send end
}
else
{
 	$response["status"]="0";
}
echo json_encode($response);

?>