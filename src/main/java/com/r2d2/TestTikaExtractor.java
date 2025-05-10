package com.r2d2;

import java.util.HashMap;
import java.util.Map;

public class TestTikaExtractor {
    public static void main(String[] args) {
        // Create an instance of the TikaContentExtractor
        TikaContentExtractor extractor = new TikaContentExtractor();
        
        // Create input as Map<String, Object> instead of JSON string
        Map<String, Object> input = new HashMap<>();
        input.put("file_url", "https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/c7ceaa4924c82986be5a73839c3eb260_chat_5ebe5626b9f1cd89fbb9f665a527591f.docx");
        
        // Call the handler method with Map input
        Map<String, Object> result = extractor.handleRequest(input, null);
        
        // If you want to display all extracted content specifically
        if (result.get("statusCode").equals(200)) {
            // Use a safer approach to handle the cast
            Object bodyObj = result.get("body");
            if (bodyObj instanceof Map) {
                @SuppressWarnings("unchecked")
                Map<String, Object> body = (Map<String, Object>) bodyObj;
                
                System.out.println("\n=== EXTRACTED TEXT ===");
                System.out.println(body.get("text"));
                
                System.out.println("\n=== HTML CONTENT ===");
                System.out.println(body.get("html"));
                
                System.out.println("\n=== METADATA ===");
                @SuppressWarnings("unchecked")
                Map<String, String> metadata = (Map<String, String>) body.get("metadata");
                if (metadata != null) {
                    for (Map.Entry<String, String> entry : metadata.entrySet()) {
                        System.out.println(entry.getKey() + ": " + entry.getValue());
                    }
                }
            }
        }
    }
}