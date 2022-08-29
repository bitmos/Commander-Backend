
# import io
# import boto3
# from PIL import Image
# from apps.TextAnalysis.TextPredict import textAnalysis
# client = boto3.client('rekognition')
# def imageocr(image_binary):
#     # image = Image.open(path)
#     # rgb_im = image.convert('RGB')
#     li=[]
#     # stream = io.BytesIO()
#     # rgb_im.save(stream,format="JPEG")
#     # image_binary = stream.getvalue()

#     response = client.detect_text(Image={'Bytes':image_binary})
#     for i in response["TextDetections"]:
#             li.append(i["DetectedText"])
#     text=(" ").join(li)
#     result=textAnalysis(text)
#     return result