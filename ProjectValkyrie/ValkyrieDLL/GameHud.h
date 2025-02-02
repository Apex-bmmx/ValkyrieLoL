#pragma once
#include "MemoryReadable.h"
#include "Vector.h"

class GameHud : public MemoryReadable {

public:
	void ReadFromBaseAddress(int baseAddr);
	bool WasChatOpenMillisAgo(int millis);

	Vector2 minimapSize;
	Vector2 minimapPosition;
	Vector3 mouseWorldPos;
	bool    isChatOpen;

private:
	int     chatLastOpenTimestamp;
};