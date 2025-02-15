'use strict'

module.exports = {
service: 'R2D2',
provider:{
  name: 'aws',
  stage: 'prod',
  region: 'eu-north-1',
  runtime: "python3.12"
  },
package: {
    patterns:['!node_modules/**','!venv/**','!my-project**','!package.json','!package-lock.json','README.md']
  },
functions:{
  extractTextFromOtherFiles:{
    handler: "extractTextFromOtherFiles.main",
    timeout: 360,
    name: `R2D2-extractTextFromOtherFiles`,
    memorySize: 512,
    description: "extracts text from docx and text files."
  },
  extractTextFromPDF:{
    handler: "extractTextFromPDF.main",
    timeout: 360,
    name: `R2D2-extractTextFromPDF`,
    memorySize: 512,
    description: "extracts text from PDF"

  },
  extractTextFromExcelFile:{
    handler: "extractTextFromExcelFile.main",
    timeout: 360,
    name: `R2D2-extractTextFromExcelFile`,
    memorySize: 512,
    description: "extracts text from Excel files"
  },
  countTokens: {
    handler: "countTokens.main",
    timeout: 30,
    name: `R2D2-countTokens`,
    memorySize: 512,
    description: "counts token of incoming text for defined model"
    
  },
  executePythonCode: {
    handler: "executePythonCode.main",
    timeout: 360,
    name: `R2D2-executePythonCode`,
    memorySize: 512,
    description: "executes Python code"
  }
},

plugins:["serverless-python-requirements"],

custom:{
pythonRequirements:{
  useDownloadCache: false, //not using cache prevents broken dependencies
  useStaticCache: false //not using cache prevents broken dependencies
}
}
}



