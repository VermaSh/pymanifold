
class FluidProperties():

	PROPERTIES = {"default":[False,False,False],
				 "water":[999.87, 18200, 0.001],
				 "mineraloil": [800, 10000000000,0.0003051],
				 "polyacrylamide":[1100, 14.28,0.003]}

	def getDensity(self, fluid_name):
		return self.PROPERTIES[fluid_name][0]

	def getResistivity(self, fluid_name):
		return self.PROPERTIES[fluid_name][1]
	
	def getViscosity(self, fluid_name):
		return self.PROPERTIES[fluid_name][2]

class ChannelTypes():
	VALID_CHANNEL_TYPES = ("rectangle")

	def getValidChannelType(self):
		return self.VALID_CHANNEL_TYPES

	def isChannelTypeValid(self, channelType):
		return channelType in self.VALID_CHANNEL_TYPES

# TODO: Tjunction

