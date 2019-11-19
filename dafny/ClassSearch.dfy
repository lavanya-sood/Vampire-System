class Search
{

  var bloodTypes: array<string>;
  var bloodExpiryDates: array<int>;
  
  predicate Valid()
  reads this;
  {
    bloodTypes != null && bloodExpiryDates != null
  }
  
  predicate hasType(a: seq<string>, bloodType: string)
  {
    forall k: int :: 0 <=k<|a| ==> a[k] == bloodType
  }

  function sum(s: array<int>, index: int ): int
  requires s != null;
  requires 0<=index<=s.Length;
  reads s;
  {
    if (index == 0) then 0 else sum(s, index-1) + s[index-1]
  }
  
  constructor ()
  ensures Valid();
  modifies this;
  {
    bloodTypes := new string[3];
    bloodTypes[0], bloodTypes[1], bloodTypes[2] := "A", "AB", "A";
    bloodExpiryDates := new int[4];
    bloodExpiryDates[0], bloodExpiryDates[1], bloodExpiryDates[2], bloodExpiryDates[3] := 20190820, 20190525, 20190907, 20191015;
  }
  
  method sumBloodQuantity (blood: array<int>) returns (amount: int)
  requires Valid(); ensures Valid();
  requires blood != null;
  ensures amount == sum(blood, blood.Length);
  {
    amount := 0;
    var i := 0;
    while (i < blood.Length) 
    invariant 0<=i<=blood.Length
    invariant amount == sum(blood, i)
    {
      amount := amount + blood[i];
      i := i + 1;
    }
  }
 
  method searchByBloodType(bloodType: string) returns (result: seq<string>)
  requires Valid(); ensures Valid();
  ensures hasType(result[..], bloodType);
  ensures |result| == multiset(bloodTypes[..])[bloodType];
  {
    var temp := new string[bloodTypes.Length];
    var i := 0;
    var j := 0;
    while (i < bloodTypes.Length && j < temp.Length) 
    invariant 0 <= i <= bloodTypes.Length
    invariant 0 <= j <= bloodTypes.Length
    invariant hasType(temp[..j], bloodType)
    invariant j == multiset(bloodTypes[..i])[bloodType]
    {
      if (bloodTypes[i] == bloodType) {
        temp[j] := bloodTypes[i];
        j := j + 1;
      }
      i := i + 1;
    }
    assert bloodTypes[..] == bloodTypes[..bloodTypes.Length];
    assert j == multiset(bloodTypes[..])[bloodType];
    result := temp[..j];
  }
  
  // need to add verification, super lost for this one :( 
  method searchBetweenRanges(blood: array<int>, start: int, end: int) returns (result: seq<int>)
  requires Valid(); ensures Valid();
  requires blood != null;
  {
    var temp := new int[blood.Length];
    var i := 0;
    var j := 0;
    while (i < blood.Length && j < blood.Length) 
    invariant 0 <= i <= blood.Length
    invariant 0 <= j <= blood.Length
    {
      if (blood[i] >= start && blood[i] <= end) {
        temp[j] := blood[i];
        j := j + 1;
      }
      i := i + 1;
    }
    result := temp[..j];
  }
  
  method searchByExpiry(start: int, end: int) returns (result: seq<int>)
  requires Valid(); ensures Valid();
  {
    result := searchBetweenRanges(bloodExpiryDates, start, end);
  }
  
  method searchByVolume(blood: array<int>, minimum: int, maximum: int) returns (result: seq<int>)
  requires Valid(); ensures Valid();
  requires blood != null;
  {
    result := searchBetweenRanges(blood, minimum, maximum);
  }
  
  method testSearchByType() 
  requires Valid(); ensures Valid();
  {
    var answer1 := searchByBloodType("A");
    assert |answer1| == multiset(bloodTypes[..])["A"];
    assert hasType(answer1, "A");
      
    var answer2 := searchByBloodType("AB");
    assert |answer2| == multiset(bloodTypes[..])["AB"];
    assert hasType(answer2, "AB");
      
    var answer3 := searchByBloodType("B");
    assert |answer3| == multiset(bloodTypes[..])["B"];
    assert hasType(answer3, "B");
  }
  
  // need to add verification
  method testSearchByExpiry()
  requires Valid(); ensures Valid();
  {
    var searchExpiry1 := searchByExpiry(20180101, 20200101);
    var searchExpiry2 := searchByExpiry(20190525, 20190525);
    var searchExpiry3 := searchByExpiry(20190501, 20190530);
    var searchExpiry4 := searchByExpiry(20180101, 20181010);
  }
  
  // add verification for searching between ranges
  method testSearchByVolume()
  requires Valid(); ensures Valid();
  {
    var A := new int[4];
    A[0], A[1], A[2], A[3] := 500, 300, 200, 100;
    var B := new int[0];
  
    var totalVolumeA := sumBloodQuantity(A);
    assert totalVolumeA == sum(A, A.Length);
    var totalVolumeB := sumBloodQuantity(B);
    assert totalVolumeB == sum(B, B.Length);
  
    var bloodSum := new int[2];
    bloodSum[0], bloodSum[1] := totalVolumeA, totalVolumeB;
    // add verification below
    var searchVolume1 := searchByVolume(bloodSum, 0, 2000);
    var searchVolume2 := searchByVolume(bloodSum, 500, 1000);
    var searchVolume3 := searchByVolume(bloodSum, 750, 2000);
  }
}
