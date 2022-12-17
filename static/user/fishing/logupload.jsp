
<%@page import="connection.Fishing"%>
<%@page import="java.sql.ResultSet"%>
<%@page import="java.sql.Statement"%>
<%@page import="java.io.FileOutputStream"%>
<%@page import="java.io.File"%>
<%@page import="org.apache.commons.fileupload.util.Streams"%>
<%@page import="java.io.InputStream"%>
<%@page import="org.apache.commons.fileupload.FileItemStream"%>
<%@page import="org.apache.commons.fileupload.FileItemIterator"%>
<%@page import="org.apache.commons.fileupload.servlet.ServletFileUpload"%>
<%@page import="java.sql.Connection"%>
<%@page import="connection.DBconnection"%>
<%
DBconnection bconnection=new DBconnection();
Connection con=bconnection.mycon();

ServletFileUpload upload=new ServletFileUpload();
FileItemIterator iter=null;
String fle=null;
String nm=null;
String pw=null;

int flg=0;

String fpth="C:\\Users\\kiranChellan\\Documents\\NetBeansProjects\\Antifishing\\";
//String fpth="C:\\Users\\Shaniba\\Documents\\NetBeansProjects\\Antifishing\\";

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
        else if(nam.equals("textfield2")){
             pw=str;
        }           
       }
       else
       {
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
                    flg=1;
            }
        }
}

if(flg==1){
    try
  {
    Statement st=con.createStatement();

    String sql="select * from login where name='"+nm+"' and password='"+pw+"' ";
    ResultSet rs= st.executeQuery(sql);
    if(rs.next())
    {
        String lgid=rs.getString(1);
        String tp=rs.getString(4);
        
        session.setAttribute("loginid", lgid); 
        session.setAttribute("type", tp);        
        
       if(tp.equalsIgnoreCase("admin")){
           
       }
        else if(tp.equalsIgnoreCase("user"))
        {                            
        String s1=fpth+"web\\image\\"+fle;
        String s2=fpth+"share2\\"+lgid+".bmp";
        
        Fishing f=new Fishing();
        String s=f.CombiningShare(fpth,s1, s2);
        
       if(s.equals(pw))
       {          
%>  
        <script type="text/javascript">
               alert("Success..\n");
               window.location="homepg.jsp";
        </script>
 <%
       }
       else{
          %>
        <script type="text/javascript">
            alert("Unknown User.\nPlease Try Again..!!<%=s%>");
               window.location="login1.jsp";
        </script>
 <%
       }
      }
    }
  }
  catch(Exception e){
  }
}


%>

