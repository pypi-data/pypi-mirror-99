"""For some raw skin, generate 1.0, 1.8 and 1.8 bedrock skins.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from sys import exit as sysexit

import layeredimage.io
import PIL
from layeredimage.layeredimage import Layer, LayeredImage
from PIL import Image

THISDIR = str(Path(__file__).resolve().parent)
from .waifu2x import load_models, upscale_image


class Namespace:
	"""Simulates argparse namespace."""

	def __init__(self, **kwargs):
		"""Simulates argparse namespace."""
		self.__dict__.update(kwargs)


def cleanImg(image: Image.Image, alphaThreshold: int = 225) -> Image.Image:
	"""Clean up semi transparent stuff when upscaling and saving with a threshold.

	Args:
		image (Image.Image): pil image to clean up
		alphaThreshold (int, optional): threshold. Defaults to 225.

	Returns:
		Image.Image: [description]
	"""
	pixdata = image.load()
	for y in range(image.size[1]):
		for x in range(image.size[0]):
			if pixdata[x, y][3] < alphaThreshold:
				image.putpixel((x, y), (0, 0, 0, 0))
			else:
				image.putpixel((x, y), pixdata[x, y][:3] + (255,))
	return image


def ver1to2(layer: Layer) -> Layer:
	"""Convert a 1.8 skin to 1.8_bedrock.

	Args:
		layer (Layer): texture layer to upscale

	Returns:
		Layer: upscaled layer
	"""
	image = layer.image
	args = Namespace(
		gpu=-1,
		method="scale",
		noise_level=1,
		color="rgb",
		model_dir=THISDIR + "/models/vgg7/",
		arch="VGG7",
		scale_ratio=2,
		tta_level=8,
		tta=False,
		block_size=128,
		batch_size=16,
	)
	model = load_models(args)
	image = cleanImg(upscale_image(args, image, model["scale"]))
	return Layer(
		layer.name,
		image,
		image.size,
		(layer.offsets[0] * 2, layer.offsets[1] * 2),
		layer.opacity,
		layer.visible,
		layer.blendmode,
	)


def ver0to1(layer: Layer) -> Layer:
	"""Convert a 1.0 skin to 1.8.

	Args:
		layer (Layer): texture layer to port

	Returns:
		Layer: ported layer
	"""
	image = layer.image
	background = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
	background.paste(image, (0, 0), image)
	return Layer(
		layer.name,
		background,
		background.size,
		(layer.offsets[0], layer.offsets[1]),
		layer.opacity,
		layer.visible,
		layer.blendmode,
	)


def ver1to0(layer: Layer) -> Layer:
	"""Convert a 1.8 skin to 1.0.

	Args:
		layer (Layer): texture layer to backport

	Returns:
		Layer: backport layer
	"""
	image = layer.image
	background = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
	background.paste(image, (0, 0), image)
	image2 = image.crop((0, 32, 64, 64))
	background.paste(image2, (0, 16), image2)
	return Layer(
		layer.name,
		background,
		background.size,
		(layer.offsets[0], layer.offsets[1]),
		layer.opacity,
		layer.visible,
		layer.blendmode,
	)


def ver2to1(layer: Layer) -> Layer:
	"""Convert a 1.8_bedrock skin to 1.8.

	Args:
		layer (Layer): texture layer to downscale

	Returns:
		Layer: downscale layer
	"""
	image = layer.image
	image.resize((64, 64))
	return Layer(
		layer.name,
		image,
		image.size,
		(layer.offsets[0], layer.offsets[1]),
		layer.opacity,
		layer.visible,
		layer.blendmode,
	)


def upgradeLayer(layer: Layer, target: int = 2) -> Layer | None:
	"""Layer to port or upgrade

	Args:
		layer (Layer): texture layer to act on
		target (int, optional): target version. Defaults to 2.

	Returns:
		Layer | None: Layer or None
	"""
	ver = getVer(layer)
	if ver == target:
		return layer
	if target == 2:
		if ver == 1:
			return ver1to2(layer)
		if ver == 0:
			layer = ver0to1(layer)
			return ver1to2(layer)
	if target == 1:
		if ver == 2:
			return ver2to1(layer)
		if ver == 0:
			return ver0to1(layer)
	if target == 0:
		if ver == 2:
			layer = ver2to1(layer)
			return ver1to0(layer)
		if ver == 1:
			return ver1to0(layer)
	return


def getVer(layer: Layer) -> int:
	"""Make a guess at the version based on the layer dimensions.

	Args:
		layer (Layer): the layer

	Returns:
		int: the estimated version
	"""
	if layer.dimensions[0] > 64 and layer.dimensions[1] > 64:
		return 2
	if layer.dimensions[1] > 32:
		return 1
	return 0


def upgradeTex(layeredImage: LayeredImage, target: int = 2) -> LayeredImage:
	"""Upgrade/ port a texture

	Args:
		layeredImage (LayeredImage): represents the texture
		target (int, optional): target version. Defaults to 2.

	Returns:
		LayeredImage: upgraded texture
	"""
	versions = {0: (64, 32), 1: (64, 64), 2: (128, 128)}
	layers = []
	for layer in layeredImage.layers:
		layers.append(upgradeLayer(layer, target))
	layeredImage.layersAndGroups = layers
	layeredImage.dimensions = versions[target]
	return layeredImage


def openRawTex(filePath: str) -> LayeredImage | None:
	"""Open texture from a file path

	Args:
		filePath (str): path

	Returns:
		LayeredImage|None: texture
	"""
	layeredImage = None
	try:
		image = Image.open(filePath)
		layeredImage = LayeredImage([Layer("layer0", image, image.size)])
	except PIL.UnidentifiedImageError:
		try:
			layeredImage = layeredimage.io.openLayerImage(filePath)
		except ValueError:
			print("Failed")
	return layeredImage


def dumpTex(filePath: str):
	"""For some raw skin, generate 1.0, 1.8 and 1.8 bedrock skins.

	Args:
		filePath (str): path to skin
	"""
	if not os.path.exists(filePath + ".d"):
		os.makedirs(filePath + ".d")
	layeredImage = openRawTex(filePath)
	ver18b = upgradeTex(layeredImage)
	layeredimage.io.saveLayerImage(filePath + ".d/18b.ora", ver18b)
	cleanImg(layeredImage.getFlattenLayers()).save(filePath + ".d/18b.png")

	ver18 = upgradeTex(layeredImage, 1)
	layeredimage.io.saveLayerImage(filePath + ".d/18.ora", ver18)
	cleanImg(layeredImage.getFlattenLayers()).save(filePath + ".d/18.png")

	ver10 = upgradeTex(layeredImage, 0)
	layeredimage.io.saveLayerImage(filePath + ".d/10.ora", ver10)
	cleanImg(layeredImage.getFlattenLayers()).save(filePath + ".d/10.png")


def cli():
	"""Cli entry point."""
	# fmt: off
	parser = argparse.ArgumentParser(description=__doc__,
		formatter_class=argparse.RawTextHelpFormatter)
	# Let's use a low severity and medium confidence by default
	parser.add_argument("filepath", help="Path to skin source")
	args = parser.parse_args()
	dumpTex(args.filepath)

	sysexit(0)
	# fmt: on
