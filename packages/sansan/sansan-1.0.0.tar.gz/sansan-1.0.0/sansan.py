class San(object):

	def san1(self,n):
		x=str(n)
		l=list(x)
		u=len(x)
		qosindi=0
		harip=""
		for i in range(u):
			if l[i].isdigit():
				qosindi += int(l[i])
		return(qosindi)