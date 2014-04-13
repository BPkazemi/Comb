from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ocr_magic import runner

# Create your views here.
def index(request):
	return render(request, 'pdfocr/index.html')

@csrf_exempt
def upload(request):
	if request.method == 'POST':
		file_contents = request.FILES
		pdf_name = str(file_contents['user-pdf'])
		
		text_array = runner.pdf_to_text(pdf_name)	
		text = ''.join(text_array)
		context = { 'text': text }

		png_filepaths = runner.pdf_to_pnglist(pdf_name)
		return StreamingHttpResponse(request, png_filepaths)
	
		# if file_contents:
		# 	return render(request, 'pdfocr/results.html', context)
		# else:
		# 	# TODO: Graceful failure
			return HttpResponse('Failed to upload file. Try again.')

def stream_response(request, png_filepaths):
    return StreamingHttpResponse(stream_response_generator(png_filepaths))

def stream_response_generator(png_filepaths):
	for index, path in enumerate(png_filepaths):
		text = runner.ocr(path)
		yield "------ PAGE {}------\n{}\n".format(index, text)
		time.sleep(1)