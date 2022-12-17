/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package connection;

/**
 *
 * @author DRUVI
 */
import java.util.Properties;
import javax.activation.DataHandler;
import javax.activation.DataSource;
import javax.activation.FileDataSource;
import javax.mail.*;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;

public class MailWithAttachment
{
public  void send( String to1,String sub ,String msg, String path,String fnm)
{
    String host = "smtp.gmail.com";//host name
    String from = "antiphisher64@gmail.com";//sender id
    String to = to1;///reciever id
    String pass = "asdfghjkl!@#";//sender's password
    String fileAttachment = path;//file name for attachment
    //system properties
    Properties prop = System.getProperties();
    // Setup mail server properties
    prop.put("mail.smtp.gmail", host);
    prop.put("mail.smtp.starttls.enable", "true");
    prop.put("mail.smtp.host", host);
    prop.put("mail.smtp.user", from);
    prop.put("mail.smtp.password", pass);
    prop.put("mail.smtp.port", "587");
    prop.put("mail.smtp.auth", "true");
    try{
    //session
    Session session = Session.getInstance(prop, null);
    // Define message
    MimeMessage message = new MimeMessage(session);
    message.setFrom(new InternetAddress(from));
    message.addRecipient(Message.RecipientType.TO,new InternetAddress(to));
    message.setSubject(sub);
    // create the message part
    MimeBodyPart messageBodyPart = new MimeBodyPart();
    //message body
    messageBodyPart.setText(msg);
    Multipart multipart = new MimeMultipart();
    multipart.addBodyPart(messageBodyPart);
    //attachment
    messageBodyPart = new MimeBodyPart();

    DataSource source = new FileDataSource(fileAttachment);
    messageBodyPart.setDataHandler(new DataHandler(source));
    messageBodyPart.setFileName(fnm);

    multipart.addBodyPart(messageBodyPart);
    message.setContent(multipart);
    //send message to reciever
    Transport transport = session.getTransport("smtp");
    transport.connect(host, from, pass);
    transport.sendMessage(message, message.getAllRecipients());
    transport.close();
    
    }catch(Exception e){
        System.out.print(e);
    }
}
}