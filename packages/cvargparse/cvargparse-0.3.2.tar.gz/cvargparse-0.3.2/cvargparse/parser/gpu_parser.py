from cvargparse.parser.base import BaseParser

class GPUParser(BaseParser):
	def __init__(self, *args, **kw):
		super(GPUParser, self).__init__(*args, **kw)
		self.add_argument(
			"--gpu", "-g", type=int, nargs="+", default=[-1],
			help="which GPU to use. select -1 for CPU only")
