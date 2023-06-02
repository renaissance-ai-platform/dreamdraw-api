
class CodeformerUpscaler:
    def upscale_image(self, image_path: str, background_enhance:bool, face_upsample: bool, upscale: int, codeformer_fidelity: int):

        from codeformer.app import inference_app

        pipe = inference_app(
            image=image_path,
            background_enhance=background_enhance,
            face_upsample=face_upsample,
            upscale=upscale,
            codeformer_fidelity=codeformer_fidelity,
        )

        return [pipe]

    