<?php
include("connection.php");
include('functions.php');

// $lid="55";
$response=array();
$lid=$_POST['userid'];
$to_acno=$_POST['to_acno'];
$ac_holder=$_POST['ac_holder'];
$sec_pin=$_POST['sec_pin'];
$amount=$_POST['amount'];

// $lid='56';
// $to_acno="788";
// $ac_holder="jjj";
// $sec_pin="12345";
// $amount=500;

$share=$_FILES['file']['name'];
move_uploaded_file($_FILES['file']['tmp_name'],"share/".$share);

//-------------------------------------------------
    $rr=mysql_query("SELECT * FROM `acc_balance`,`user` WHERE `user_id`='$lid' AND acc_balance.`acc_no`=`user`.`acc_no`");
    if(mysql_num_rows($rr)>0)
    { 
      $x=mysql_fetch_array($rr);
      $from_acno=$x['acc_no'];
      if(($x["balance"]-$amount)>0)
      {    
//-------------------------------------------------------------------------------------------
//-------------------------------------------------------------------------------------------
        $cipher = "aes-128-cbc";
        $ivlen = openssl_cipher_iv_length($cipher);

    $qr="SELECT * FROM skeys WHERE `sid`='$lid'";
    
    $re=mysql_query($qr);
    if(mysql_num_rows($re)>0)
    {   
        // echo "hiiiiiii--------"."<br>";
        $res=mysql_fetch_array($re);
        // echo "------------".$res["sid"]."<br>";
        // echo $res["iv"]."<br>";
        // echo $res["skey"]."<br>";

        $ssiv = base64_decode($res["iv"]);
        $sskey = base64_decode($res["skey"]);
        //----------------------------------------------
        
        // echo$ssiv.";;;;;;;;;;;;;<br>";
    
      $share1="share/".$lid."_shr1.jpg";
      $share2="share/".$lid."_shr2.jpg";
      $im1 = file_get_contents($share1);
        $im2 = file_get_contents($share2);
        // echo $im1."*****--------"."<br>";

        // $dcd=base64_decode($first400.$theRest);
        $dcd=base64_decode($im1.$im2);

        // echo "==========--------"."<br>";
        //decrpyt and display
        // $img = openssl_decrypt($dcd, $cipher, $key, $options=0, $iv);
        $img = openssl_decrypt($dcd, $cipher, $sskey, $options=0, $ssiv);
        file_put_contents("bbbbbbbb.jpg", $img);
//-------------------------------------------------
//extract password

  $src = 'C:\wamp\www\antiphishing\AndroidConnections\bbbbbbbb.jpg';
  $im = imagecreatefrompng($src);
        // echo "111111111111111--------"."<br>";

  $real_message = '';

  for($x=0;$x<100;$x++){
      $y = $x;
      $rgb = imagecolorat($im,$x,$y);
      $r = ($rgb >>16) & 0xFF;
      $g = ($rgb >>8) & 0xFF;
      $b = $rgb & 0xFF;
  
      $blue = toBin($b);
      $real_message .= $blue[strlen($blue)-1];
  }
  $real_message = toString($real_message);

  // $real_message


  // $real_message = substr($real_message, 0,strlen($real_message)-1);
    // echo "00000000000000000--------"."<br>";
    // echo $real_message;

    // echo substr($real_message, 0,strlen($real_message)-1);

//-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------
    // $sq="SELECT * FROM `login` WHERE `login_id`='$lid' AND `password`='$real_message'";
    $sq="SELECT * FROM `login` WHERE `login_id`='$lid'";
    $rre=mysql_query($sq);
    if(mysql_num_rows($rre)>0)
    {
        $x=mysql_fetch_array($rre);
        $pd=$x["password"];
        $ln=strlen($pd);
        if($ln>6){
          $pd=substr($pd, 0,6);
          $real_message=substr($real_message, 0,6);
        }
        else{
          $pd=substr($pd, 0,$ln);
          $real_message=substr($real_message, 0,$ln);
        }
        if($pd==$real_message){
          mysql_query("UPDATE `acc_balance` SET `balance`=`balance`-'$amount' WHERE `acc_no`='$from_acno'");
          mysql_query("UPDATE `acc_balance` SET `balance`=`balance`+'$amount' WHERE `acc_no`='$to_acno'");
          $response["status"]="1";
        }
        else{
          $response["status"]="0";
        }
    }
    else{
      $response["status"]="0";
    }
//-----------------------------------------------------------------------------------------
}
else{
  $response["status"]="2";
}
}
else{
  $response["status"]="3";
}


	//---------------------------------------------------------------------------------------
		}
    else{
      $response["status"]="4";
    }

echo json_encode($response);

?>