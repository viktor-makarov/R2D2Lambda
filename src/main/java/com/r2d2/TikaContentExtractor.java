package com.r2d2;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.sax.BodyContentHandler;
import org.apache.tika.sax.ToHTMLContentHandler;
import org.xml.sax.SAXException;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class TikaContentExtractor implements RequestHandler<Map<String, Object>, Map<String, Object>> {

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
            Map<String, Object> extractionResults = extractAllContent(fileContent);
            
            body.put("text", extractionResults.get("text"));
            body.put("html", extractionResults.get("html"));
            body.put("metadata", extractionResults.get("metadata"));
            body.put("success", 1);
            response.put("statusCode", 200);
            response.put("body", body);
        } catch (Exception e) {
            if(context != null) {
                context.getLogger().log("Error: " + e.getMessage());
            } else {
                System.err.println("Error: " + e.getMessage());
            }
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
    
    /**
     * Extracts text, HTML content, and metadata from the file in a more efficient manner.
     * We still need multiple parse operations but reuse the byte array and metadata.
     * 
     * @param fileContent The binary content of the file
     * @return A map containing extracted text, HTML content, and metadata
     */
    private Map<String, Object> extractAllContent(byte[] fileContent) throws IOException, TikaException, SAXException {
        Map<String, Object> results = new HashMap<>();
        Metadata metadata = new Metadata();
        ParseContext context = new ParseContext();
        AutoDetectParser parser = new AutoDetectParser();
        
        // Extract text and collect metadata in the first pass
        BodyContentHandler textHandler = new BodyContentHandler(-1);
        try (InputStream stream = new ByteArrayInputStream(fileContent)) {
            parser.parse(stream, textHandler, metadata, context);
            results.put("text", textHandler.toString());
        }
        
        // Extract HTML in the second pass (reusing the metadata)
        ToHTMLContentHandler htmlHandler = new ToHTMLContentHandler();
        try (InputStream stream = new ByteArrayInputStream(fileContent)) {
            parser.parse(stream, htmlHandler, metadata, context);
            results.put("html", htmlHandler.toString());
        }
        
        // Process metadata that was collected during parsing
        Map<String, String> metadataMap = new HashMap<>();
        for (String name : metadata.names()) {
            metadataMap.put(name, metadata.get(name));
        }
        results.put("metadata", metadataMap);
        
        return results;
    }
}