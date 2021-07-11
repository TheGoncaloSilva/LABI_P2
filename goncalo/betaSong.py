import wave

w1 = wave.open("./sounds/dog-barking-twice.wav")
w2 = wave.open("./sounds/fast-rocket-whoosh_2.wav")

#get samples formatted as a string.
samples1 = w1.readframes(w1.getnframes())
samples2 = w2.readframes(w2.getnframes())
params = w1.getparams()
#takes every 2 bytes and groups them together as 1 sample. ("123456" -> ["12", "34", "56"])
samples1 = [samples1[i:i+2] for i in range(0, len(samples1), 2)]
samples2 = [samples2[i:i+2] for i in range(0, len(samples2), 2)]

#convert samples from strings to ints
def bin_to_int(bin):
    as_int = 0
    for char in bin[::-1]: #iterate over each char in reverse (because little-endian)
        #get the integer value of char and assign to the lowest byte of as_int, shifting the rest up
        as_int <<= 8
        as_int += ord(char) 
    return as_int

samples1 = [bin_to_int(s) for s in samples1] #['\x04\x08'] -> [0x0804]
samples2 = [bin_to_int(s) for s in samples2]

#average the samples:
samples_avg = [(s1+s2)/2 for (s1, s2) in zip(samples1, samples2)]
final = samples_avg
output = wave.open("out-test", 'wb')
output.setparams(params)
for i in range(len(final)):
    output.writeframes(final[i][1])
output.close()