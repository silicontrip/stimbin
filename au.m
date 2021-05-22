#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
#import <AppKit/AppKit.h>
#import <Kernel/math.h> // math.h

// gcc -o au au.m -framework Foundation -framework AppKit -framework AVFoundation

double pa[3][1280][720];

int main(int argc, const char *argv[])
{

	NSLog(@"every program needs an arg count: %d",argc);

	for (int carg = 1; carg < argc; ++carg)
	{
		NSAutoreleasePool* splash = [NSAutoreleasePool new];

		NSString *file = [NSString stringWithUTF8String:argv[carg]];
		NSURL *fileUrl = [NSURL fileURLWithPath:file];

		NSError* readError;
		AVAudioFile* aFile = [[[AVAudioFile alloc] initForReading:fileUrl error:&readError] autorelease];

		NSUInteger imx = 1280;
		NSUInteger imy = 720;



		if (aFile)
		{
			// NSLog(@"af: %@",aFile);
			AVAudioFramePosition aLen = aFile.length;
		//	NSLog(@"len: %lld",aLen);
			AVAudioFormat * aFormat = [aFile processingFormat];

			if (aFormat.channelCount == 2 )
			{
			//	NSLog(@"format: %@",[aFormat settings]);
			//	NSLog(@"process %@",[[aFile processingFormat] settings]);

				AVAudioPCMBuffer*  audioData = [[[AVAudioPCMBuffer alloc] initWithPCMFormat:aFormat frameCapacity:aLen] autorelease];

			//	NSLog(@"frame length: %u",audioData.frameLength);
			//	NSLog(@"Frame capacity: %u",audioData.frameCapacity);

				@try {
					BOOL ok = [aFile readIntoBuffer:audioData  error:&readError];

					if (ok) {
						NSLog(@"Audio File %@ read.",file);
						// - (BOOL)readIntoBuffer:(AVAudioPCMBuffer *)buffer error:(NSError **)outError;

						for (int rgb=0; rgb <3; ++rgb)
							for (int x =0; x< imx; ++x)
								for (int y=0; y<imy; ++y)
									pa[rgb][x][y]=0;

					//	int16_t * __nonnull const * __nullable i16Buffer = [audioData int16ChannelData];
						float * __nonnull const * __nullable fBuffer = [audioData floatChannelData];
					//	int32_t * __nonnull const * __nullable i32Buffer = [audioData int32ChannelData];


					//	NSLog(@"16 data: %x",(unsigned int)i16Buffer);
					//	NSLog(@"f data: %x",(unsigned int)fBuffer);
					//	NSLog(@"32 data: %x",(unsigned int)i32Buffer);

						float * fdata = *fBuffer;
					//NSLog(@"idata: %x",(unsigned int)fdata);

						NSBitmapImageRep *outrep = [[NSBitmapImageRep alloc]
							initWithBitmapDataPlanes: NULL
							pixelsWide: imx
							pixelsHigh: imy
							bitsPerSample: 8
							samplesPerPixel: 3
							hasAlpha: NO
							isPlanar: NO
							colorSpaceName: NSDeviceRGBColorSpace
							bytesPerRow: 1280 * 3
							bitsPerPixel: 24];

						double scaley = (imy-1) / 2.0 ;
						double scalex = 1.0 * (imx-1) / aLen;
			
						for (NSUInteger ax = 0; ax < aLen ; ++ax)
						{

							float lval = *(fdata + ax);
							float rval = *(fdata + aLen + ax);

							//double phaseangle = atan2(lval,rval);
							//double phaseangle = atan2(fabs(lval),fabs(rval));
							double phaseangle = atan2(lval+1.0,rval+1.0);

							double hue = (phaseangle + M_PI) / (2 * M_PI);

							NSColor* phCol = [NSColor colorWithHue:hue saturation:1 brightness:1 alpha:1];

							CGFloat red;
							CGFloat green;
							CGFloat blue;
							CGFloat alpha;

							[phCol getRed:&red green:&green blue:&blue alpha:&alpha];

							NSUInteger x = lround (ax * scalex);
							NSUInteger y = lround((lval + 1.0 ) * scaley);

						// NSLog(@"X: %lu y: %lu rgb: %f %f %f",x,y,red,green,blue);


							pa[0][x][y] += red;
							pa[1][x][y] += green;
							pa[2][x][y] += blue;

							NSUInteger y2 = (lval + 1.0 ) * scaley;

							pa[0][x][y2] += red;
							pa[1][x][y2] += green;
							pa[2][x][y2] += blue;

							//NSLog(@"%lu: %f - %f\n",(unsigned long)ii,lval,rval);
						}

						NSLog(@"Finished Conversion.");

						double maxval = 0;

						for (int px =0; px < imx; ++px)
						{
							for (int py=0; py< imy; ++py)
							{
								if (pa[0][px][py] > maxval)
									maxval= pa[0][px][py];
								if (pa[1][px][py] > maxval)
									maxval= pa[1][px][py];
								if (pa[2][px][py] > maxval)
									maxval= pa[2][px][py];
							}
						}	

						for (int px =0; px < imx; ++px)
						{
							for (int py=0; py< imy; ++py)
							{
								double r = pow((pa[0][px][py]/maxval),0.3);
								double g = pow((pa[1][px][py]/maxval),0.3);
								double b = pow((pa[2][px][py]/maxval),0.3);

								//NSLog(@"rgb: %f %f %f",pa[0][px][py],pa[1][px][py],pa[2][px][py]);
								NSColor* setCol = [NSColor colorWithDeviceRed:r green:g blue:b alpha:1.0];
								[outrep setColor:setCol atX:px y:py];
							}
						}	

						NSDictionary* prop = nil;
						NSData *dd = [outrep representationUsingType:NSPNGFileType properties:prop];
						NSString* fn = [NSString stringWithFormat:@"%@.png",file];
						[dd writeToFile:fn atomically: NO];

					}
				} @catch (NSException* e) {
					NSLog(@"error: %@",e.name);
					NSLog(@"reason: %@",e.reason);
					NSLog(@"info: %@",e.userInfo);
				}
			}
		}
			[splash release];

	}
}
