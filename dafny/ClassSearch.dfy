class Search
{

  var bloodTypes: array<string>;
  
  predicate Valid()
  reads this;
  {
    bloodTypes != null
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
  
  predicate sorted(a: array<int>, l: int, u: int)
  reads a
  requires a != null
  {
    forall i, j :: 0 <= l <= i <= j <= u < a.Length ==> a[i] <= a[j]
  }

  predicate partitioned(a: array<int>, i: int)
  reads a
  requires a != null
  {
    forall k, k' :: 0 <= k <= i < k' < a.Length ==> a[k] <= a[k']
  }
  
  constructor ()
  ensures Valid();
  modifies this;
  {
    bloodTypes := new string[3];
    bloodTypes[0], bloodTypes[1], bloodTypes[2] := "A", "AB", "A";
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

  method BubbleSort(a: array<int>)
  requires Valid(); ensures Valid();
  modifies a;
  requires a != null
  ensures sorted(a, 0, a.Length-1)
  {
    var i := a.Length - 1;
    while(i > 0)
      invariant i < 0 ==> a.Length == 0 // ask
      invariant sorted(a, i, a.Length-1)
      invariant partitioned(a, i)
      {
        var j := 0;
        while (j < i)
          invariant 0 < i < a.Length && 0 <= j <= i
          invariant sorted(a, i, a.Length-1)
          invariant partitioned(a, i)
          invariant forall k :: 0 <= k <= j ==> a[k] <= a[j]
          {
            if(a[j] > a[j+1])
            { a[j], a[j+1] := a[j+1], a[j]; }
              j := j + 1;
          }
          i := i -1;
      }
  }
  
  method findLowerLimit(a: array<int>, start: int) returns (minimum: int)
  requires Valid(); ensures Valid()
  requires a != null
  requires sorted(a, 0, a.Length)
  ensures 0<=minimum<=a.Length
  ensures minimum == a.Length ==> forall k: int :: 0<=k<a.Length ==> a[k] < start
  ensures forall k: int :: 0<=k<minimum ==> a[k] < start
  {
    minimum := a.Length;
    var i := 0;
    while (i < a.Length) 
    invariant 0 <= i <= a.Length
    invariant forall k: int :: 0<=k<i ==> a[k] < start
    {
      if (a[i] >= start) {
        minimum := i;
        break;
      }
      i := i + 1;
    }
  }

  method findUpperLimit(a: array<int>, end: int) returns (maximum: int)
  requires Valid(); ensures Valid()
  requires a != null
  requires sorted(a, 0, a.Length)
  ensures 0<= maximum <= a.Length
  ensures forall k: int :: 0<=k<maximum ==> a[k] <= end
  {
    maximum := a.Length;
    var i := 0;
    while (i < a.Length) 
    invariant 0 <= i <= a.Length
    invariant forall k: int :: 0<=k<i ==> a[k] <= end
    {
      if (a[i] > end) {
        maximum := i;
        break;
      }
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
  
  method testSearchByExpiry()
  requires Valid(); ensures Valid();
  {
    var bloodExpiryDates := new int[4];
    bloodExpiryDates[0], bloodExpiryDates[1], bloodExpiryDates[2], bloodExpiryDates[3] := 20190820, 20190525, 20190907, 20191015;
  
    BubbleSort(bloodExpiryDates);
    assert sorted(bloodExpiryDates, 0, bloodExpiryDates.Length);
    
    var minimum := findLowerLimit(bloodExpiryDates, 20180101);
    var maximum := findUpperLimit(bloodExpiryDates, 20200101);
    assert forall k: int :: 0<=k<minimum ==> bloodExpiryDates[k] < 20180101;
    assert forall k: int :: 0<=k<maximum ==> bloodExpiryDates[k] <= 20200101;
    
    minimum := findLowerLimit(bloodExpiryDates, 20180101);
    maximum := findUpperLimit(bloodExpiryDates, 20181010);
    assert forall k: int :: 0<=k<minimum ==> bloodExpiryDates[k] < 20180101;
    assert forall k: int :: 0<=k<maximum ==> bloodExpiryDates[k] <= 20181010;
  }
  
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
    bloodSum[0], bloodSum[1] := totalVolumeB, totalVolumeA;
    
    BubbleSort(bloodSum);
    assert sorted(bloodSum, 0, bloodSum.Length);
    
    var minimum := findLowerLimit(bloodSum, 0);
    var maximum := findUpperLimit(bloodSum, 2000);
    assert forall k: int :: 0<=k<minimum ==> bloodSum[k] < 0;
    assert forall k: int :: 0<=k<maximum ==> bloodSum[k] <= 2000;
    
    minimum := findLowerLimit(bloodSum, 500);
    maximum := findUpperLimit(bloodSum, 1000);
    assert forall k: int :: 0<=k<minimum ==> bloodSum[k] < 500;
    assert forall k: int :: 0<=k<maximum ==> bloodSum[k] <= 1000;
    
    minimum := findLowerLimit(bloodSum, 750);
    maximum := findUpperLimit(bloodSum, 2000);
    assert forall k: int :: 0<=k<minimum ==> bloodSum[k] < 750;
    assert forall k: int :: 0<=k<maximum ==> bloodSum[k] <= 2000;
    
    minimum := findLowerLimit(bloodSum, 8000);
    maximum := findUpperLimit(bloodSum, 8000);
    assert forall k: int :: 0<=k<minimum ==> bloodSum[k] < 8000;
    assert forall k: int :: 0<=k<maximum ==> bloodSum[k] <= 8000;
    
  }
}
