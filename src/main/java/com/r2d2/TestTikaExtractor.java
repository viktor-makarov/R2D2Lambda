package com.r2d2;

import java.util.HashMap;
import java.util.Map;

public class TestTikaExtractor {
    public static void main(String[] args) {
        // Create an instance of the TikaTextExtractor
        TikaTextExtractor extractor = new TikaTextExtractor();
        
        // Create input as Map<String, Object> instead of JSON string
        Map<String, Object> input = new HashMap<>();
        input.put("file_url", "https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/text_pdf.pdf");
        
        // Call the handler method with Map input
        Map<String, Object> result = extractor.handleRequest(input, null);
        
        // Print the result
        System.out.println("Status code: " + result.get("statusCode"));
        System.out.println("Body: " + result.get("body"));
        
        // If you want to display the extracted text specifically
        if (result.get("statusCode").equals(200)) {
            // Use a safer approach to handle the cast
            Object bodyObj = result.get("body");
            if (bodyObj instanceof Map) {
                @SuppressWarnings("unchecked")
                Map<String, Object> body = (Map<String, Object>) bodyObj;
                System.out.println("\nExtracted text: \n" + body.get("text"));
            }
        }
    }
}