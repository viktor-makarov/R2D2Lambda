'use strict'

const stages = {
  dev: {
    logLevel: 'DEBUG',
  },
  prod: {
    logLevel: 'INFO'
  }
}

module.exports = {
service: 'R2D2',
provider:{
  name: 'aws',
  stage: "${opt:stage, 'dev'}",
  region: 'eu-north-1',
  environment: {
    STAGE: "${opt:stage, 'dev'}",
    LOG_LEVEL: "${self:custom.currentStage.logLevel}"
  }
  },
package: {
    excludeDevDependencies: false,
    patterns:['!node_modules/**','!venv/**','!my-project**','!package.json','!package-lock.json','README.md']
  },
functions:{
  extractTextFromOtherFiles:{
    runtime: "python3.12",
    handler: "extractTextFromOtherFiles.main",
    timeout: 360,
    name: "R2D2-extractTextFromOtherFiles",
    memorySize: 512,
    description: "extracts text from docx and text files."
  },
  extractTextWithTika:{
    runtime: "java17",
    handler: "com.r2d2.TikaTextExtractor::handleRequest",
    timeout: 360,
    name: "R2D2-extractTextWithTika",
    memorySize: 512,
    description: "extracts text from various file formats using Apache Tika"
  },
  extractTextFromPDF:{
    runtime: "python3.12",
    handler: "extractTextFromPDF.main",
    timeout: 360,
    name: `R2D2-extractTextFromPDF`,
    memorySize: 512,
    description: "extracts text from PDF"
  },
  extractTextFromExcelFile:{
    runtime: "python3.12",
    handler: "extractTextFromExcelFile.main",
    timeout: 360,
    name: `R2D2-extractTextFromExcelFile`,
    memorySize: 512,
    description: "extracts text from Excel files"
  },
  countTokens: {
    runtime: "python3.12",
    handler: "countTokens.main",
   // provisionedConcurrency: 2,     // <- вот эта строка
    timeout: 30,
    name: `R2D2-countTokens`,
    memorySize: 512,
    description: "counts token of incoming text for defined model"
    
  },
  executePythonCode: {
    runtime: "python3.12",
    handler: "executePythonCode.main",
    timeout: 360,
    name: `R2D2-executePythonCode`,
    memorySize: 512,
    description: "executes Python code"
  }
},

plugins:["serverless-python-requirements"],

custom:{
currentStage: "${self:custom.stages.${self:provider.stage}}",
stages: stages,
pythonRequirements:{
  useDownloadCache: false, //not using cache prevents broken dependencies
  useStaticCache: false //not using cache prevents broken dependencies
}
}
}




