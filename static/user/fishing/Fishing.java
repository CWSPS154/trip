
package connection;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.awt.Graphics2D;
import javax.imageio.ImageIO;
import java.io.File;
import java.awt.image.WritableRaster;
import java.awt.image.DataBufferByte;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
/*
 *
 * @author RISS6
 */
public class Fishing {
    /**
     * @param args the command line arguments
    */
    public static BufferedImage b2,b3;
    public static void main(String[] args) {
        try {
            ////Data hiding in image
            String  file_name   = "D:\\login.JPG";
            BufferedImage   image_orig  = getImage(file_name);
            //user space is not necessary for Encrypting
            BufferedImage image = user_space(image_orig);
            image = add_textsr(image,"Haiii missu...");
            
            File f=new File("D:\\abc111.bmp");
            ImageIO.write(image,"bmp",f);
                        
            BufferedImage   image_orig2  = getImage("D:\\abc111.bmp");
            byte[] dd1= gettext(image_orig2);
            
            String ss1=new String(dd1);
            
            ss1= ss1.trim();
            System.out.print(ss1);            
            
            //////sharing of images
            String  file_name1   = "D:\\abc111.bmp";
            BufferedImage   image_orig1  = user_space(getImage(file_name1));
            
            b2=new BufferedImage(image_orig.getWidth(), image_orig.getHeight(), BufferedImage.TYPE_INT_ARGB);
            b3=new BufferedImage(image_orig.getWidth(), image_orig.getHeight(), BufferedImage.TYPE_INT_ARGB);
            Shares(image_orig2);
            
    //===========================================================================================================
                        
           BufferedImage bmp= combineshares(b2, b3);
           BufferedImage image1  = getImage("D:\\share1plusshare2.bmp");
           BufferedImage   image_orig3  = getImage("D:\\share1plusshare2.bmp");
           
            byte[] dd= gettext(image_orig3);
            String ss=new String(dd);            
            ss= ss.trim();
            System.out.print(ss);            
        }
        catch (IOException ex) {
           System.out.print(ex.getMessage()+"");    
        }
     }

    public String CombiningShare(String fpath,String s1,String s2){
     //       String  s1   = "D:\\share1.bmp";
     //       String  s2   = "D:\\share2.bmp";
                        
            BufferedImage   im1  = getImage(s1);
            BufferedImage   im2  = getImage(s2);
            //user space is not necessary for Encrypting
            
            for(int m=0;m<im1.getWidth();m++)
          {
                for(int m1=0;m1<im1.getHeight();m1++)
                {
                     int rgb = im1.getRGB(m, m1);
                     Color aa= new Color(rgb);
                     int r =aa.getRed();
                     int g = aa.getGreen();
                     int b =aa.getBlue();
                     int r1=(r & 240);
                     int r2=(r & 15);
                     int g1=(g & 240);
                     int g2=(g & 15);
                     int bl1=(b & 240);
                     int bl2=(b & 15);
                                          
                    Color rgb1=new Color(r1, g1, bl1,aa.getAlpha());
                  //  Color rgb2=new Color(r2, g2, bl2,aa.getAlpha());
                    im1.setRGB(m, m1, rgb1.getRGB());
                 //   im2.setRGB(m, m1, rgb2.getRGB());
                }
          }
              
            for(int m=0;m<im2.getWidth();m++)
          {
                for(int m1=0;m1<im2.getHeight();m1++)
                {
                     int rgb = im2.getRGB(m, m1);
                     Color aa= new Color(rgb);
                     int r =aa.getRed();
                     int g = aa.getGreen();
                     int b =aa.getBlue();
                     int r1=(r & 240);
                     int r2=(r & 15);
                     int g1=(g & 240);
                     int g2=(g & 15);
                     int bl1=(b & 240);
                     int bl2=(b & 15);
                                          
                  //  Color rgb1=new Color(r1, g1, bl1,aa.getAlpha());
                    Color rgb2=new Color(r2, g2, bl2,aa.getAlpha());
                 //   im1.setRGB(m, m1, rgb1.getRGB());
                    im2.setRGB(m, m1, rgb2.getRGB());
                }
          }                       
            
            BufferedImage b1 = user_space(im1);
            BufferedImage b2 = user_space(im2);
                   
            BufferedImage bmp= combineshares(b1, b2);
            BufferedImage   image_orig3  = getImage(fpath+"share1plusshare2.bmp");
           
            byte[] dd= gettext(image_orig3);
            String ss=new String(dd);            
            ss= ss.trim();
        //    System.out.print(ss); 
        
        return ss;
    }     
    
    public String CreateShares(String fpath,String tpath,String pwd,String id){
        String re="na";
        try{
            
             String  file_name   = fpath;
            BufferedImage   image_orig  = getImage(file_name);
            //user space is not necessary for Encrypting
            BufferedImage image = user_space(image_orig);
            image = add_textsr(image,pwd);
            
            File f=new File(tpath+"abc111.bmp");
            ImageIO.write(image,"bmp",f);
                        
            BufferedImage   image_orig2  = getImage(tpath+"abc111.bmp");
            byte[] dd1= gettext(image_orig2);
            
            String ss1=new String(dd1);
            
            ss1= ss1.trim();
            System.out.print(ss1);            
            
            //////sharing of images
            String  file_name1   = tpath+"abc111.bmp";
            BufferedImage   image_orig1  = user_space(getImage(file_name1));
            
            b2=new BufferedImage(image_orig1.getWidth(), image_orig1.getHeight(), BufferedImage.TYPE_INT_ARGB);
            b3=new BufferedImage(image_orig1.getWidth(), image_orig1.getHeight(), BufferedImage.TYPE_INT_ARGB);
            
            Shares(b2,b3,image_orig1,id,tpath);
            re="ok";
        }
        catch(Exception e){
            re="na";
        }
         return re; 
    }

     public  static void  Shares(BufferedImage b5,BufferedImage b6,BufferedImage image,String id,String tpth)
     {
      try {
          for(int m=0;m<image.getWidth();m++)
          {
                for(int m1=0;m1<image.getHeight();m1++)
                {
                     int rgb = image.getRGB(m, m1);
                     Color aa= new Color(rgb);
                     int r =aa.getRed();
                     int g = aa.getGreen();
                     int b =aa.getBlue();
                     int r1=(r & 240);
                     int r2=(r & 15);
                     int g1=(g & 240);
                     int g2=(g & 15);
                     int bl1=(b & 240);
                     int bl2=(b & 15);
                    
                    Color rgb1=new Color(r1, g1, bl1,aa.getAlpha());
                    Color rgb2=new Color(r2, g2, bl2,aa.getAlpha());
                    b5.setRGB(m, m1, rgb1.getRGB());
                    b6.setRGB(m, m1, rgb2.getRGB());
                }
           }
           File f=new File(tpth+"share1\\"+id+".bmp");
           ImageIO.write(user_space(b5),"bmp",f);
           
           File f1=new File(tpth+"share2\\"+id+".bmp");
           ImageIO.write(user_space(b6),"bmp",f1);
      }
      catch (Exception ex) {
          //Logger.getLogger(Imaging2Shares.class.getName()).log(Level.SEVERE, null, ex);
      }
  }
   public static BufferedImage getImage(String f)
   {
       BufferedImage image   = null;
       File file    = new File(f);
       try
       {
            image = ImageIO.read(file);
       }
       catch(Exception ex)
       {
       }
       return image;
   }
   private static  BufferedImage user_space(BufferedImage image)
   {
        BufferedImage new_img  = new BufferedImage(image.getWidth(), image.getHeight(), BufferedImage.TYPE_3BYTE_BGR);
	Graphics2D graphics   = new_img.createGraphics();
	graphics.drawRenderedImage(image, null);
	graphics.dispose(); 
	return new_img;
    }
    private boolean setImage(BufferedImage image, File file, String ext)
    {
        try
        {
            file.delete(); //delete resources used by the File
            ImageIO.write(image,ext,file);
            return true;
        }
        catch(Exception e)
        {
            return false;
        }

    }
    
    public static   byte[] gettext(BufferedImage borig)
    {   int dk=0;
        byte[] d=new byte[100000];
        int k=0;
        int annd=1;
        int shft=0;
        try{
        for(int m=0;m<borig.getWidth();m++)
          {
                for(int m1=0;m1<borig.getHeight();m1++)
                {
                     int rgb = borig.getRGB(m, m1);
                     Color aa= new Color(rgb); 
                     int red =aa.getRed();
                     red=red & annd;
                    // red=red<<shft;
                     dk=d[k];
                   //  dk=(byte)(dk<< 1);
                     red=red<<shft;
                     dk=(byte)(dk | (byte)red);
                   
                     d[k]=(byte)dk;
                     shft=shft+1;
                     if(shft==8)
                     {
                         d[k]=(byte)dk;
                         shft=0;
                         annd=1;
                         k++;
                     }
                             
                }
          }
        }
        catch(Exception ex)
        {}
        return d;
        
    }
    
     public  static  BufferedImage add_textsr(BufferedImage sh1, String text)
    {
        //convert all items to byte arrays: image, message, message length
      
       byte msg[] = text.getBytes();
       int k=0;
       int shift=0;
       BufferedImage borig=new BufferedImage(sh1.getWidth(),sh1.getHeight(), BufferedImage.TYPE_3BYTE_BGR);
       try
       {      
          try {
          for(int m=0;m<borig.getWidth();m++)
          {
                for(int m1=0;m1<borig.getHeight();m1++)
                {
                     int rgb = sh1.getRGB(m, m1);
                 
                     Color aa= new Color(rgb);
                  
                     int kk=msg[k];
                     kk=kk>>shift;
                     
                     int red =aa.getRed();
                     int green = aa.getGreen();
                     int blue =aa.getBlue();
                     
                     int msgbit= (kk & 1);
                     //int lm=msgbit>>shift;
                     shift=shift+1;
                     
                     if(shift==8)
                     {
                         k++;
                         shift=0;
                     }
                     int rednew= red & 254;
                     rednew=rednew | msgbit;
                     
                    Color clrorg= new Color(rednew, green,blue,aa.getAlpha());
                    borig.setRGB(m, m1, clrorg.getRGB());                     
                }
          }
       }
       catch(Exception ex)
       {           
       }          
//       File f=new File("D:\\share1plusshare2.bmp");
//       ImageIO.write(borig,"bmp",f);
            
      } catch (Exception ex) {
         // Logger.getLogger(Imaging2Shares.class.getName()).log(Level.SEVERE, null, ex);
      }
       return borig;
    }
    
    public  static  BufferedImage add_text(BufferedImage image, String text)
    {
        //convert all items to byte arrays: image, message, message length
        byte img[]  = get_byte_data(image);
        byte msg[] = text.getBytes();
        byte len[]   = bit_conversion(msg.length);
        try
        {
            encode_text(img, len,  0); //0 first positiong
            encode_text(img, msg, 32); //4 bytes of space for length: 4bytes*8bit = 32 bits
        }
        catch(Exception e)
        {
        }
        return image;
    }
    public static   byte[] get_byte_data(BufferedImage image)
    {
        WritableRaster raster   = image.getRaster();
        DataBufferByte buffer = (DataBufferByte)raster.getDataBuffer();
        return buffer.getData();
    }
     public static byte[] bit_conversion(int i)
    {
        byte byte3 = (byte)((i & 0xFF000000) >>> 24); //0
        byte byte2 = (byte)((i & 0x00FF0000) >>> 16); //0
        byte byte1 = (byte)((i & 0x0000FF00) >>> 8 ); //0
        byte byte0 = (byte)((i & 0x000000FF)       );
        return(new byte[]{byte3,byte2,byte1,byte0});
    }
   public static byte[] encode_text(byte[] image, byte[] addition, int offset)
    {
        //check that the data + offset will fit in the image
        if(addition.length + offset > image.length)
        {
            throw new IllegalArgumentException("File not long enough!");
        }
      //loop through each addition byte
        for(int i=0; i<addition.length; ++i)
        {
            //loop through the 8 bits of each byte
            int add = addition[i];
            for(int bit=7; bit>=0; --bit, ++offset) //ensure the new offset value carries on through both loops
            {
                //assign an integer to b, shifted by bit spaces AND 1
                //a single bit of the current byte
                int b = (add >>> bit) & 1;
                //assign the bit by taking: [(previous byte value) AND 0xfe] OR bit to add
                //changes the last bit of the byte in the image to be the bit of addition
                image[offset] = (byte)((image[offset] & 0xFE) | b );
            }
        }
        return image;
    }

    
    public static  byte[] decode_text(byte[] image)
    {
     int length = 0;
     int offset  = 32;
     //loop through 32 bytes of data to determine text length
      for(int i=0; i<32; ++i) //i=24 will also work, as only the 4th byte contains real data
      {
          length = (length << 1) | (image[i] & 1);
      }
      byte[] result = new byte[length];
      //loop through each byte of text
      for(int b=0; b<result.length; ++b )
      {
          for(int i=0; i<8; ++i, ++offset)
          result[b] = (byte)((result[b] << 1) | (image[offset] & 1));
      }
       return result;
     }
      ////////////////sharing and combining 
  public static BufferedImage combineshares(BufferedImage sh1,BufferedImage sh2)
  {
      BufferedImage borig=new BufferedImage(sh1.getWidth(),sh1.getHeight(), BufferedImage.TYPE_INT_RGB);
       try {
          for(int m=0;m<borig.getWidth();m++)
          {
                for(int m1=0;m1<borig.getHeight();m1++)
                {
                     int rgb = sh1.getRGB(m, m1);
                     int rgb1=sh2.getRGB(m, m1);
                     Color aa= new Color(rgb);
                     Color ab=new Color(rgb1);
                     
                     int rsh1 =aa.getRed();
                     int gsh1 = aa.getGreen();
                     int bsh1 =aa.getBlue();
                     
                     int rsh2 =ab.getRed();
                     int gsh2 = ab.getGreen();
                     int bsh2 =ab.getBlue();
  
                     int orgred=(rsh1) | rsh2;
                     int orggreen=(gsh1) | gsh2;
                     int orblue=(bsh1) | bsh2;
                     
                      Color clrorg= new Color(orgred, orggreen,orblue,aa.getAlpha());
                     borig.setRGB(m, m1, clrorg.getRGB());
                     
                }
          }
          
          
            File f=new File("D:\\share1plusshare2.bmp");
            ImageIO.write(borig,"bmp",f);
            
            
      } catch (IOException ex) {
         // Logger.getLogger(Imaging2Shares.class.getName()).log(Level.SEVERE, null, ex);
      }
       return borig;
     
  }
 public  static void  Shares(BufferedImage image)
  {
      try {
          for(int m=0;m<image.getWidth();m++)
          {
                for(int m1=0;m1<image.getHeight();m1++)
                {
                     int rgb = image.getRGB(m, m1);
                     Color aa= new Color(rgb);
                     int r =aa.getRed();
                     int g = aa.getGreen();
                     int b =aa.getBlue();
                     int r1=(r & 240);
                     int r2=(r & 15);
                     int g1=(g & 240);
                     int g2=(g & 15);
                     int bl1=(b & 240);
                     int bl2=(b & 15);
                                          
                    Color rgb1=new Color(r1, g1, bl1,aa.getAlpha());
                    Color rgb2=new Color(r2, g2, bl2,aa.getAlpha());
                    b2.setRGB(m, m1, rgb1.getRGB());
                    b3.setRGB(m, m1, rgb2.getRGB());
                }
          }          
          
            File f=new File("D:\\share1.bmp");
            ImageIO.write(user_space(b2),"bmp",f);
            
            File f1=new File("D:\\share2.bmp");
            ImageIO.write(user_space(b3),"bmp",f1);            
            
      }
      catch (Exception ex) {
          //Logger.getLogger(Imaging2Shares.class.getName()).log(Level.SEVERE, null, ex);
      }
      
      
      
  }  
    
    /////////////////////////////////////
    
    
    
    
    
    
    
    
  
}
   