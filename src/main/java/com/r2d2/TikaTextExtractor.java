package com.r2d2;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.sax.BodyContentHandler;
import org.xml.sax.SAXException;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class TikaTextExtractor implements RequestHandler<Map<String, Object>, Map<String, Object>> {

    @Override
    public Map<String, Object> handleRequest(Map<String, Object> input, Context context) {
        Map<String, Object> response = new HashMap<>();
        Map<String, Object> body = new HashMap<>();
        
        String fileUrl = (String) input.get("file_url");
        if (fileUrl == null) {
            body.put("error", "No file URL provided");
            body.put("success", 0);
            response.put("statusCode", 500);
            response.put("body", body);
            return response;
        }
        
        try {
            byte[] fileContent = downloadFile(fileUrl);
            String extractedText = extractText(fileContent);
            
            body.put("text", extractedText);
            body.put("success", 1);
            response.put("statusCode", 200);
            response.put("body", body);
        } catch (Exception e) {
            context.getLogger().log("Error: " + e.getMessage());
            body.put("error", e.getMessage());
            body.put("success", 0);
            response.put("statusCode", 500);
            response.put("body", body);
        }
        
        return response;
    }
    
    private byte[] downloadFile(String fileUrl) throws IOException {
        URL url = new URL(fileUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        
        if (connection.getResponseCode() != HttpURLConnection.HTTP_OK) {
            throw new IOException("Failed to download file: " + connection.getResponseCode() + " " + connection.getResponseMessage());
        }
        
        try (InputStream inputStream = connection.getInputStream()) {
            return inputStream.readAllBytes();
        }
    }
    
    private String extractText(byte[] fileContent) throws IOException, TikaException, SAXException {
        BodyContentHandler handler = new BodyContentHandler(-1); // -1 means no limit on output size
        Metadata metadata = new Metadata();
        ParseContext context = new ParseContext();
        AutoDetectParser parser = new AutoDetectParser();
        
        try (InputStream stream = new ByteArrayInputStream(fileContent)) {
            parser.parse(stream, handler, metadata, context);
            return handler.toString();
        }
    }
}