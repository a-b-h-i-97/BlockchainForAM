pragma solidity 0.4.25;

contract owned {
    address owner;
    constructor() public { owner = msg.sender; }
    
}


contract mortal is owned {
    function kill() public {
        if (msg.sender == owner) selfdestruct(owner);
    }
}

contract DesignDB is owned,mortal{

    struct fileVersion
    {
        string fileHash;
        string version;
        uint timestamp;
    }
    struct DesignFile
    {
        string fileName;
        fileVersion current;
        fileVersion[] history;
        address designer;
    }

    

    DesignFile[] public files;

    function addDesign(string fileName,string fileHash, string version) public
    {//require instead of if
        int i = findDesign(fileHash);
        require(i == -1, "File with same hash should not exist in db");
        fileVersion memory v = fileVersion(fileHash,version,now);
        files.length++;
        DesignFile storage f = files[files.length-1];
        f.current = v;
        f.fileName = fileName;
        f.designer = msg.sender;
        // files.push(DesignFile({current:v,history:new fileVersion[](0),designer:msg.sender}));

    }

    function getFilesLength() public view returns (uint)
    {
        return files.length;
    }

    function getDesign(uint index) public view returns (address,string,string,string,uint)
    {
        DesignFile memory f = files[index];
        return (f.designer,f.fileName,f.current.fileHash,f.current.version,f.current.timestamp);
    }

    function getHistoryLength(uint index) public view returns(uint)
    {
        return files[index].history.length;
    }

    function getHistory(uint fIndex,uint index) public view returns (string,string,uint)
    {
        fileVersion memory v = files[fIndex].history[index];
        return (v.version,v.fileHash,v.timestamp);
    }




    
    function findDesign(string fileHash) public view returns (int)
    {
        for(uint i = 0; i<files.length;i++)
        {
            bytes memory hash = bytes(files[i].current.fileHash);
            if(keccak256(hash) == keccak256(bytes(fileHash)))
                return int(i);
            for(uint j = 0; j<files[i].history.length;j++)
            {
                bytes memory oldHash = bytes(files[i].history[j].fileHash);
                if(keccak256(oldHash) == keccak256(bytes(fileHash)))
                    return int(i);
            }
            
        }

        return -1;
    }           

    function modifyDesign(uint index, string newFileHash, string newVersion) public
    {
        
        DesignFile storage f = files[index];
        require(f.designer==msg.sender, "Design can only be modified by designer");
        int i = findDesign(newFileHash);
        if(i != -1)
        {
            return;
        }
        f.history.push(f.current);
        f.current = fileVersion(newFileHash, newVersion, now);
    }


}




