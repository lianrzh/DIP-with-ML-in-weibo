import Image
import math

# The Segment of Image Process

# Function: openImg
#   Open the image in the same schema (RGB and 256x256)
#	Parameters:
#		imgName:String	the name of the image
#	Return:
#		the Image Object
def openImg( imgName ):
	return Image.open(imgName).resize((256,256)).convert('RGB')

# Function: split
#	Split the Image
#	Parameters:
#		img:Image	the image
#		size:truple	the size of image
#	Return:
#		the array of the splited images
def split( img, size=(32,32)):
	w, h = img.size
	sw, sh = size 
	return [img.crop((i, j, i+sw, j+sh)).copy() \
				for i in xrange(0, w, sw) \
				for j in xrange(0, h, sh)]

# Function: rgb2hsi
#	Transfore the rgb to hsi
#	Parameters:
#		rgbImg:Image	the image of rgb
#	Return:
#		the imgage of hsi
def rgb2hsi( rgbImg ):
	#rgbImg = openImg("CBIRdataset/images/900.jpg")
	rgbMat = list(rgbImg.getdata())
	hsiMat = list()
	for i in rgbMat:
		R = i[0]/255.0
		G = i[1]/255.0
		B = i[2]/255.0
		
		h = (180/math.pi) * math.acos(0.5*((R-G)+(R-B))/(math.sqrt((R-G)*(R-G)+(R-B)*(G-B))+0.000001))
		if B > G:
			h = 360 - h
		s = 1 - 3/(R+G+B+0.000001)*min((R,G,B))
		i = sum((R,G,B))/3.0
		hsiMat.append((h,s,i))
		# Here here
	return hsiMat

# Function: getCharacteristics
# 	Get the characteristics of 12 partions
#	Parameters:
#		imgArr:Image	the arr of 16x16 images splited from a image
#	Return:
#		the characteristics of 12 partions
def getCharacteristics( img ):
	# the partion array
	partion = ( \
		[0],\
		[7],\
		[56],\
		[63],\
		(8,16,24,32,40,48),\
		(1,2,3,4,5,6),\
		(15,23,31,39,47,55),\
		(57,58,59,60,61,62),\
		(9,10,11,17,18,19,25,26,27,28,35,36),\
		(12,13,14,20,21,22,29,30,27,28,35,36),\
		(33,34,41,42,43,49,50,51,27,28,35,36),\
		(37,38,44,45,46,52,53,54,27,28,35,36) )
	# sqlit the image	
	imgArr = split( img )
	# get the characteristics
	imgChar_12 = list()
	for i in xrange(12):
		arr_72 = statitict( imgArr, partion[i] )
		imgChar_12.append( arr_72 )
	return imgChar_12
	
def statitict( imgArr, nums ):
	H = [0, 0, 0, 0, 0, 0, 0, 0]
	S = [0, 0 ,0]
	I = [0, 0, 0]	
	# statitic HSI
	for i in nums:
		hsiMat = rgb2hsi( imgArr[i] )
		for point in hsiMat:
			# statitict the H
			if point[0] >= 21 and point[0] <= 40:
				H[1] += 1
			elif point[0] >= 41 and point[0] <= 75:
				H[2] += 1
			elif point[0] >= 76 and point[0] <= 155:
				H[3] += 1
			elif point[0] >= 156 and point[0] <= 190:
				H[4] += 1
			elif point[0] >= 191 and point[0] <= 270:
				H[5] += 1
			elif point[0] >= 271 and point[0] <= 295:
				H[6] += 1
			elif point[0] >= 296 and point[0] <= 315:
				H[7] += 1
			else:
				H[0] += 1	
			# statitict the S
			if point[1] >= 0 and point[1] < 0.2:
				S[0] += 1
			elif point[1] >= 0.2 and point[1] < 0.7:
				S[1] += 1
			else:
				S[2] += 1
			# statitict the I
			if point[2] >= 0 and point[2] < 0.2:
				I[0] += 1
			elif point[2] >= 0.2 and point[2] < 0.7:
				I[1] += 1
			else:
				I[2] += 1
	# calculate the arr72
	# motify here
	arr72 = H
	arr72.append(S[0])
	arr72.append(S[1])
	arr72.append(S[2])
	arr72.append(I[0])
	arr72.append(I[1])
	arr72.append(I[2])
	return arr72	

# Funciton: calculate
#	The main calculator
#	Parameters:
#		curImg:Image	the cur image
#		img:Image		the matching image
#	Return:
#		the same rate
def calculate( curImgChar_12, img, weight ):
	imgChar_12 = getCharacteristics( img )
	# calculating the likehoods
	likehoods = list()
	for i in xrange(12):
		x = curImgChar_12[i]
		y = imgChar_12[i]
		xAver = sum( x ) / 72.0
		yAver = sum( y ) / 72.0
		r = sum((xi-xAver)*(yi-yAver) for xi, yi in zip(x,y)) / math.sqrt(sum((xi-xAver)*(xi-xAver) for xi in x)*sum((yi-yAver)*(yi-yAver) for yi in y))
		likehoods.append( r )
	# calculating the total same rate
	rate = weight[0] * sum(likehoods[i] for i in xrange(4)) + weight[1] * sum(likehoods[i+4] for i in xrange(4)) + weight[2] * sum(likehoods[i+8] for i in xrange(4))
	#print rate
	return rate

# Function getWeightArr
#	Get the Weights from the file
#	Parameters:
#		label:String	the label name
#	Return:
#		the array of weight
def getWeightArr( label ):
	fobj = open("weight/"+ label+".txt", 'r')
	arr = list()
	for eachLine in fobj:	
		arr.append(float(eachLine))
	fobj.close()
	return arr

# Function: searcher
# 	The main function to search the image
#	Parameters:
#		src_address:String		the address of the source image
#		search_adress:String	the search address
#		num_imgs:int			how many images are in the search address
#		num_match:int			how many images you want to return
#	Return:
#		the idx of the matching images
def searcher( src_address, search_adress, label, num_imgs, num_match ):
	# get the characteristics of cur image
	cur = openImg( src_address+'0.jpg');
	curImgChar_12 = getCharacteristics( cur )
	# calculate the rate
	weight = getWeightArr(label)
	imgs = searcherForTaining( src_address, search_adress, weight, curImgChar_12, num_imgs, num_match )

	res = sorted(imgs, key=lambda x: x['rate'], reverse=True )	
	#cur.show();
	
	#print "Result:"
	#for i in range(num_match):
	#	res[i]['imgObj'].show()

	resArr = list()
	for i in xrange(num_match):
		resArr.append(res[i]['idx'])
	
	return resArr, res
	
# Function: searcherForTaining
#	The process of the function searcher
#	Parameters:
#		src_address:String		the address of the source image
#		search_adress:String	the search address
#		weight:array			the weight array
#		curImgChar_12:array		the array of characteristic
#		num_imgs:int			how many images are in the search address
#		num_match:int			how many images you want to return
#	Return:
#		the image after processing		
def searcherForTaining( src_address, search_adress, weight, curImgChar_12, num_imgs, num_match=0 ):
	imgs = list()
	for i in range(num_imgs):
		imgName = search_adress+'%d.jpg' % (i)
		item = dict()
		img = openImg(imgName)
		item['imgObj'] = img
		item['idx'] = i
		imgs.append(item)
	# calculate the rate
	for item in imgs:
		rate = calculate(curImgChar_12, item['imgObj'], weight)
		item['rate'] = rate
	return imgs;
	
if __name__ == '__main__':
	searcher("CBIRdataset/images/", "CBIRdataset/images/", "0", 100, 10)
	

