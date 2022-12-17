<%@page import="connection.Fishing"%>
<%@page import="connection.Seedblocks"%>
<%@page import="connection.MailWithAttachment"%>
<%@page import="connection.ImagePixs"%>
<%@page import="java.awt.Graphics"%>
<%@page import="java.awt.image.BufferedImage"%>
<%@page import="com.mysql.jdbc.Statement"%>
<%@page import="com.sun.org.apache.bcel.internal.generic.AALOAD"%>
<%@page import="javax.imageio.ImageIO"%>
<%@page import="java.io.ByteArrayOutputStream"%>
<%@page import="connection.DBconnection"%>
<%@page import="java.sql.ResultSet"%>
<%@page import="java.io.FileInputStream"%>
<%@page import="java.sql.Connection"%>
<%@page import="java.io.FileOutputStream"%>
<%@page import="java.io.File"%>
<%@page import="org.apache.commons.fileupload.util.Streams"%>
<%@page import="java.io.InputStream"%>
<%@page import="org.apache.commons.fileupload.FileItemStream"%>
<%@page import="org.apache.commons.fileupload.FileItemIterator"%>
<%@page import="org.apache.commons.fileupload.servlet.ServletFileUpload"%>
<%
DBconnection bconnection=new DBconnection();
Connection con=bconnection.mycon();

ServletFileUpload upload=new ServletFileUpload();
FileItemIterator iter=null;
String fle=null;
String nm=null;
String acc=null;
String gender=null;
String addr=null;
String email=null,pass=null,cpass=null;

String fpth="C:\\Users\\kiranChellan\\Documents\\NetBeansProjects\\Antifishing\\";
//String fpth="C:\\Users\\ABDULLAH\\Documents\\NetBeansProjects\\Antifishing\\";

iter=upload.getItemIterator(request);
while(iter.hasNext()){
    FileItemStream item=iter.next();
    String nam=item.getFieldName();
    InputStream stream=item.openStream();
    if(item.isFormField()){
        String str=Streams.asString(stream);
        if(nam.equals("textfield")){
            nm=str;
        }
         else if(nam.equals("radiobutton")){
             gender=str;
         }
          else if(nam.equals("textfield2")){
             acc=str;
          }
          else if(nam.equals("textfield3")){
             addr=str;
          }
          else if(nam.equals("textfield4")){
             email=str;
          }
          else if(nam.equals("textfield5")){
             pass=str;
          }  
          else if(nam.equals("textfield6")){
             cpass=str;
          }   
       }
       else {
               if(item.getName()!=""){
                    fle=item.getName().substring(item.getName().lastIndexOf("\\") + 1);
                    File f=new File(fpth+"web\\image\\"+fle);
         
                    if(!f.exists()){
                        f.createNewFile();
                    }
                    FileOutputStream fos=new FileOutputStream(f);
                    int ch;
                    while((ch=stream.read())!=-1){
                        fos.write(ch);
                    }
            }
        }
}

java.sql.Statement s=con.createStatement();
if(pass.equals(cpass)){
    //select * from registrn where acnumber=''
    int sst=0;
    ResultSet rs1=s.executeQuery("select * from registrn where acnumber='"+acc+"'");
    if(rs1.next()){
               
    %>
<script type="text/javascript">
    alert("Check Your Account number..!!!");
    window.location="registration.jsp";
</script>
<%
    }
       else{
    ResultSet rs=s.executeQuery("select * from login where name='"+email+"'");
    if(rs.next()){
%>


<script type="text/javascript">
    alert("Choose a Different Image or Email-ID !!!");
    window.location="registration.jsp";
</script>
<%
    }
       else{
            
            s.executeUpdate("insert into login(name,password)values('"+email+"','"+pass+"')",Statement.RETURN_GENERATED_KEYS);
            int logid=0;
            rs=s.getGeneratedKeys();
            if(rs.next()){
                logid=rs.getInt(1);
            }
            s.executeUpdate("insert into registrn(userid,name,gender,acnumber,address,email,image)values('"+logid+"','"+nm+"','"+gender+"','"+acc+"','"+addr+"','"+email+"','"+fle+"')");

  //           Seedblocks shr=new Seedblocks();
  //           String res=shr.CreateShares("C:\\Users\\ABDULLAH\\Documents\\NetBeansProjects\\Antifishing\\web\\image\\"+fle,"C:\\Users\\ABDULLAH\\Documents\\NetBeansProjects\\Antifishing\\",pass+"",logid+"");
        Fishing f=new Fishing();
        String res=f.CreateShares(fpth+"web\\image\\"+fle,fpth,pass, logid+"");
        
        if(res.equalsIgnoreCase("ok")) {  
              
        MailWithAttachment ml=new MailWithAttachment();               
        ml.send(email, logid+"", "save it", fpth+"share1\\"+logid+".bmp",logid+".bmp");
              
%>  
 <script type="text/javascript">
               alert("Upload Successful");
               window.location="login1.jsp";
 </script>
 <%
 }
  else{
  %>  
 <script type="text/javascript">
               alert("Failed..!!");
               window.location="registration.jsp";
 </script>
 <%              
// }
 }}
    }

 }
 %>
