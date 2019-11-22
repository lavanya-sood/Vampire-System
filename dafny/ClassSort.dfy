class Sort
{

  var a: array<int>;
  
  predicate Valid()
  reads this;
  {
    a != null
  }
    
  constructor (input: array<int>)
  requires input != null;
  ensures Valid();
  modifies this;
  ensures a == input;
  {
    a := input;
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

  method BubbleSort()
  requires Valid(); ensures Valid();
  modifies a
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
              {
                a[j], a[j+1] := a[j+1], a[j];
              }
              j := j + 1;
          }
          i := i - 1;
      }
  }
    
}

method main (){
    // test 1
    var a := new int[5];
    a[0], a[1], a[2], a[3], a[4] := 20190211, 20200120, 20191203, 20191127, 20200101;
    assert a[0] == 20190211;
    assert a[1] == 20200120;
    assert a[2] == 20191203;
    assert a[3] == 20191127;
    assert a[4] == 20200101;
    var sort := new Sort(a);
    assert sort.a[0] == 20190211;
    assert sort.a[1] == 20200120;
    assert sort.a[2] == 20191203;
    assert sort.a[3] == 20191127;
    assert sort.a[4] == 20200101;
    assert sort.a.Length == 5;
    // array unsorted before calling Bubblesort()
    assert !sort.sorted(sort.a, 0, sort.a.Length - 1);
    sort.BubbleSort();  
    // array is sorted
    assert sort.sorted(sort.a, 0, sort.a.Length - 1);
    
    // test 2
    var a1 := new int[5];
    a1[0], a1[1], a1[2], a1[3], a1[4] := 20130111, 20100913, 20210203, 20191230, 20200101;
    assert a1[0] == 20130111;
    assert a1[1] == 20100913;
    assert a1[2] == 20210203;
    assert a1[3] == 20191230;
    assert a1[4] == 20200101;
    var sort1 := new Sort(a1);
    assert sort1.a[0] == 20130111;
    assert sort1.a[1] == 20100913;
    assert sort1.a[2] == 20210203;
    assert sort1.a[3] == 20191230;
    assert sort1.a[4] == 20200101;
    assert sort1.a.Length == 5;
    assert !sort1.sorted(sort1.a, 0, sort1.a.Length - 1);
    sort1.BubbleSort();  
    assert sort1.sorted(sort1.a, 0, sort1.a.Length - 1);
}

