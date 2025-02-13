'''This is a class called lin_alg with several methods designed to do matrix calculations and other linear algebra operations. About half of
of the class is what was tunred in for the Gaussian Elimination Project, but I decided to expand the class into a broader linear algebra class so 
I can use it in the future, and I needed to re-use some of the code. The area blocked off between #----------# in the class is the part that was not 
turned in previously, and the bottom of the file is completely new as well.'''
import random
from copy import deepcopy
import numpy as np
import numpy.linalg as LA

#declare class
class lin_alg:
    #This method generates a random gaussian matrix that is m by n dimensionsal, given by the arguments m and n.
    def random_matrix(self,m,n):
        rand_matrix = []
        for i in range(0,m):
            row_list = []
            for j in range(0,n):
                row_list.append(random.gauss(0,10))
            rand_matrix.append(row_list)
        return rand_matrix
    #This method generates a random gaussian vector that is n dimensional, given by the argument n.
    def random_vector(self, n):
        rand_vector= []
        for i in range(0,n):
            rand_vector.append(random.gauss(0,10))
        return rand_vector
    #This method combines the random vector and matrix from the previous two methods into a linear system.
    def random_gaussian_system(self, matrix, vector):
        random_gaussian_system = []
        if len(matrix) == len(vector):
            for index in range(0,len(vector)):
                random_gaussian_system.append(matrix[index]+[vector[index]])
        else:
            raise Exception("Dimensions of vector and matrix are not compatible.")
        return random_gaussian_system
    #This method prints the matrices in the script in a visually understandable way.
    def print_matrix(self, matrix, rounded=bool):
        print('____________________________')
        for row in matrix:
            for entry in row:
                if rounded ==True:
                    print(round(entry,3), end = ' ')
                else:
                    print(entry, end = ' ')
            print('\n')
        print('____________________________')
    #This method prints the vectors in a visually understandable way.
    def print_vector(self, vector, rounded=bool):
        for entry in vector:
            if rounded == True:
                print(round(entry,3))
            else:
                print(entry)
        print('\n')
    #This method implements an algorithm to solve for the RREF form of a given matrix, It also has two optional arguments to return
    # an inverted matrix or to return the rank of a matrix.
    def RREF(self, matrix,identity=[], invert=False, Rank=False):
        # This is a nested function to take a given value in a row and divide that row by the value to create a pivot.
        def __make_pivot(row_index, entry, matrix, identity, invert):
            scalar = 1/(entry)
            for i in range(0, len(matrix[row_index])):
                matrix[row_index][i] = round(scalar*matrix[row_index][i],15)
                if invert == True:
                    identity[row_index][i] = round(scalar*identity[row_index][i],15)
        #This method uses row operations to clear out the column underneath a pivot.
        def __clear_under_pivot(row_index, column_index, matrix, identity, invert):
            for i in range(row_index+1, len(matrix)):
                scalar = -1*matrix[i][column_index]
                for j in range(0,len(matrix[i])):
                    matrix[i][j] = matrix[i][j] + scalar*matrix[row_index][j]
                    if invert == True:
                        identity[i][j] = identity[i][j] + scalar*matrix[row_index][j]
        #This method uses row operations to clear out the column above a pivot.
        def __clear_above_pivot(row_index, column_index, matrix, identity, invert):
            for i in range(row_index-1, -1, -1):
                scalar = -1*matrix[i][column_index]
                for j in range(0,len(matrix[i])):
                    matrix[i][j] = matrix[i][j] + scalar*matrix[row_index][j]
                    if invert == True:
                        identity[i][j] = identity[i][j] + scalar*matrix[row_index][j]
        if invert == True:
            identity = self.make_identity(matrix)
        row_index = 0
        pivot_count  = 0
        for row in matrix:
            column_index = 0
            for entry in row:
                if entry != 0:
                    __make_pivot(row_index, entry, matrix, identity, invert)
                    __clear_under_pivot(row_index, column_index, matrix, identity, invert)
                    __clear_above_pivot(row_index, column_index, matrix, identity, invert)
                    pivot_count += 1
                    break
                column_index += 1
            row_index+=1
        if Rank:
            return pivot_count
        if invert == True:
            return identity
        return matrix
    #THis method tests to see whether a given system is consistent or not.
    def is_consistent(self, matrix):
        consistent = True
        for row in matrix:
            if row == [0.0 for x in range(0,len(row)-1)] + [row[-1]]:
                consistent = False
        return consistent
    #This method implements the RREF method and then prints the solution vector.
    def solve_linear_system(self, matrix):
        matrix = self.RREF(matrix)
        if self.is_consistent(matrix):
            solution_vector = [0 for x in matrix[0][:-1]]
            for row in matrix:
                pivot_position = 0
                for entry in row:
                    if entry == 1.0:
                        solution_vector[pivot_position] = row[-1]
                        break
                    pivot_position += 1
            self.print_matrix(matrix)
            self.print_vector(solution_vector)
        else:
            raise Exception("Linear system is inconsistent.")
    #This method generates an identity matrix that is of the same dimension as a given matrix.
    def make_identity(self, matrix):
        identity = []
        for i in range(0,len(matrix)):
            row = []
            for j in range(0,len(matrix)):
                if i==j:
                    row.append(1.0)
                else:
                    row.append(0.0)
            identity.append(row)
        return identity
    #This method tests to see whether or not a matrix is invertible.
    def is_invertible(self, matrix):
        matrix_copy = deepcopy(matrix)
        identity = self.make_identity(matrix_copy)
        if len(matrix) != len(matrix[0]):
            return False
        elif self.RREF(matrix_copy) != identity:
            return False
        return True
    #This method implements the RREF method to invert a square matrix if it is invertible.
    def invert_square(self, matrix):
        if self.is_invertible(matrix):
            self.print_matrix(matrix, rounded=True)
            inverse = self.RREF(matrix, invert=True)
            self.print_matrix(inverse, rounded=True)
        else: 
            print('error')
            print(len(matrix))
            self.print_matrix(matrix,rounded=True)
            self.print_matrix(self.RREF(matrix), rounded=True)
            raise Exception('Matrix is not square, or not invertible')
    #This method performs LU decompisiton on a given matrix, and returns L and U.
    def LU_decomp(self, matrix):
        L = self.make_identity(matrix)
        U = matrix
        def __clear_under_pivot(row_index, column_index, entry, L, U):
            for i in range(row_index+1, len(U)):
                scalar = -1*matrix[i][column_index]/entry
                L[i][column_index] = scalar
                for j in range(0,len(matrix[i])):
                    matrix[i][j] = matrix[i][j] + scalar*matrix[row_index][j]
        row_index = 0
        for row in matrix:
            column_index = 0
            for entry in row:
                if row_index == column_index:
                    __clear_under_pivot(row_index, column_index, entry, L, U)
                    break
                column_index += 1
            row_index += 1
        return L, U
    
#--------------------------------------------------------------------------------------------------------------------------------------#    

#This method performs an inner product on two vectors. The current innner product is the simple dot product but it could be changed as needed.
    def inner_product(self, v_1, v_2):
        if len(v_1) == len(v_2):
            inner_product = 0
            for i in range(0,len(v_1)):           
                inner_product += (v_1[i]) * (v_2[i])
            return inner_product
        else:
            raise Exception('Error: two vectors must be the same length for inner product')

#This method returns the square root of the inner product of a vector with itself.    
    def norm(self, v):
        return np.sqrt(self.inner_product(v,v))
#This method implements the graham schmidt algorithm on a given basis.        
    def gram_schmidt_alg(self, basis):
        orthonormal_basis = []
        v_1 = basis[0]
        e_1 = [x/self.norm(v_1) for x in v_1]
        orthonormal_basis.append(e_1)
        for i in range(1, len(basis)):
            f_i = basis[i]
            for j in range(0, len(orthonormal_basis)):
                temp_vec = [x*self.inner_product(basis[i], orthonormal_basis[j]) for x in orthonormal_basis[j]]
                f_i = [f_i[k] - temp_vec[k] for k in range(0,len(f_i))]
            e_i = [x/self.norm(f_i) for x in f_i]
            orthonormal_basis.append(e_i)
        return orthonormal_basis

#This method returns the conjugate transpose of a matrix.
    def conjugate(self, matrix):
        conjugate_mat = [[] for x in matrix[0]]
        for column in range(0,len(matrix[0])):
            for row in matrix:
                conjugate_mat[column].append(row[column])
        return conjugate_mat

#This method implements an algorithm to multiply two matrices.
    def mat_multiply(self, A,B):
        conj_B = self.conjugate(B)
        product = [[] for x in A]
        for row1 in range(0,len(A)):
            for row2 in range(0,len(conj_B)):
                product[row1].append(self.inner_product(A[row1], conj_B[row2]))
        return product

#This method returns a vector multiplied with a matrix.
    def mat_vec_multiply(self, matrix, vector):
        product = []
        if len(vector) != len(matrix[0]):
            raise Exception(f"{len(vector)} dimensional vector and {len(matrix)} by {len(matrix[0])} matrix cannot be multiplied.")
        for row in matrix:
            product.append(self.inner_product(row, vector))
        return product
    
    def scalar_mat_multiply(self, scalar, matrix):
        for i in range(0, len(matrix)):
            for j in range(0,len(matrix[0])):
                matrix[i][j] = scalar * matrix[i][j]
        return matrix


#This method uses the RREF method to return the rank of a matrix.
    def rank(self, A):
        return self.RREF(deepcopy(A), Rank=True)

    def is_symmetric(self, matrix):
        if len(matrix) != len(matrix[0]):
            return False
        for i in range(0,len(matrix)):
            for j in range(0,len(matrix)):
                if matrix[i][j] != matrix[j][i]:
                    return False
        return True

#This method takes a matrix listed by columns and returns that same matrix listed by rows.
    def columns_to_rows(self, matrix):
        new_mat = [[] for x in matrix[0]]
        for row_i in range(0, len(new_mat)):
            for column in matrix:
                new_mat[row_i].append(column[row_i])
        return new_mat
    
#This method takes a matrix listed by rows and returns that same matrix listed by columns.
    def rows_to_column(self, matrix):
        new_mat = [[] for x in matrix[0]]
        for column_i in range(0, len(new_mat)):
            for row in matrix:
                new_mat[column_i].append(row[column_i])
        return new_mat

#This method returns the Singular Value Decomposition of a matrix.
    def SVD(self, matrix):
        eigvals, eigvecs = LA.eig(self.mat_multiply(self.conjugate(matrix), matrix))
        p = min(len(matrix), len(matrix[0])) 
        r = self.rank(matrix)
        eigvecs_col = []
        for i in range(0,len(eigvecs[0])):
            eigvecs_col.append(list(eigvecs[:,i]))
        list1 = list(eigvals)
        combined = list(zip(list1, eigvecs_col))
        sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True)
        sorted_eig_vals, V_star = zip(*sorted_combined)
        U_columns = []
        for j in range(0,len(matrix)):
            if j < r:
                scalar = (1/np.sqrt(sorted_eig_vals[j]))
                u_j = [scalar*x for x in self.mat_vec_multiply(matrix, V_star[j])]    
            else:
                u_j = [1 if x==j else 0 for x in range(0, len(U_columns[0]))]
            U_columns.append(u_j)
        U = self.columns_to_rows(self.gram_schmidt_alg(U_columns))
        sigma = []
        for m in range(0,len(matrix)):
            sigma_row = [np.sqrt(sorted_eig_vals[x]) if x==m else 0 for x in range(0,len(matrix[0]))]
            sigma.append(sigma_row)
        return U, sigma, list(V_star)
    
    #This method computes the sum of a list. (python wasn't playing nicely)
    def _sum(self, _list):
        counter = 0
        for i in _list:
            counter += float(i)
        return counter

    #This method computes the mean of a list.
    def mean(self, _list):
        return self._sum(_list)/len(_list)
    
    #This method computes the standard deviation of  a list.
    def standard_deviation(self, _list):
        i=0
        mean = self.mean(_list)
        for x in _list:
            i += (int(x)-mean)*(int(x)-mean)
        return np.sqrt(i/(len(_list)-1))
    
    #This method standardizes and mean centers a matrix.
    def standardize_matrix(self, matrix):
        X = self.rows_to_column(matrix)
        new_X = []
        for column in X:
            new_column = [(x-self.mean(column))/self.standard_deviation(column) for x in column]
            new_X.append(new_column)
        return self.columns_to_rows(new_X)

    #This method performs Eigendecomposition of the covariance matrix of a given matrix by using SVD.
    #If project is false it returns V, D, and V_star. If project is true it returns the data matrix X, the feature vector V, and the latent 
    #representation Z.
    def Eig_Decomp_S(self, matrix, project=False, tolerance=0.0):
        X = self.standardize_matrix(matrix)
        _,S,V_star = self.SVD(X)
        if project:
            total_eigs = 0
            pruned_V_star = deepcopy(V_star)
            S_squared = self.mat_multiply(self.conjugate(S),S)
            for row in S_squared:
                for entry in row:
                    total_eigs += entry
            for row_i in range(0,len(S_squared)):
                if self._sum(S_squared[row_i])/total_eigs < tolerance:
                    pruned_V_star[row_i] = [0 for x in pruned_V_star[row_i]]
            return X, self.conjugate(pruned_V_star), self.mat_multiply(X, self.conjugate(pruned_V_star))
        return self.conjugate(V_star), self.mat_multiply(self.conjugate(S),S), self.scalar_mat_multiply(1/(len(matrix)-1), V_star)
    
    #This computes the average reconstruction error of a reconstructed data matrix.
    def avg_reconstruct_err(self, X, W):
        counter = 0
        total_err = 0
        for i in range(0,len(X)):
            for j in range(0, len(X[i])):
                total_err += abs((X[i][j]-W[i][j]))
                counter += 1
        return total_err/counter

''''
#This is a script that demonstrates the use of the class object lin_alg. It generates a random gaussian matrix and then performs 
# several linear algebra operations on it. The first two functions demonstrate the use of the SVD and eigendecomposition methods, 
# and the third function demonstrates the use of the autoencoder method.

#---------------------------------------------------------------------------------------------------------------------------------#
#This function takes a randomy generated gaussian matrix that is 40 by 20 and computes the singular value decomposition of it.
def SVD_example(mat):
    U, Sigma, V_star = op.SVD(mat)
    print(("The singular value decomposition of our matrix is: \n"))
    print('U=\n')
    op.print_matrix(U, rounded=True)
    print('Sigma = \n')
    op.print_matrix(Sigma, rounded=True)
    print('Conjugate Transpose of V is: \n')
    op.print_matrix(V_star, rounded=True)

#This function does the same as above with eigendecomposition instead of SVD
def eig_decomp_example(mat):
    V, D, V_star = op.Eig_Decomp_S(mat, project=False)
    print(("The eigendecomposition of our matrix is: \n"))
    print('V=\n')
    op.print_matrix(V, rounded=True)
    print('D = \n')
    op.print_matrix(D, rounded=True)
    print('Conjugate Transpose of V is: \n')
    op.print_matrix(V_star, rounded=True)

#This function is a dummy version of an auto encoder mdoule that might apper in a Recurrent Neural Network. It uses principle component analysis to 
#reduce the dimensionality of the data matrix by producing a latent representation and the reconstructing the data matrix. It then calculates the 
#average reconstruction error.
def auto_encoder_decoder_example(mat):
    tol = 0.01
    X, V, Z = op.Eig_Decomp_S(mat, project=True, tolerance=tol)
    print('Encoding and decoding of our matrix through PCA is as follows:\n')
    print(f'Our feature vector with low variability eigenvectors (tolerance={tol}) removed is:\n')
    op.print_matrix(V, rounded=True)
    print("The latent representation of our matrix (projection onto principle compoents) is:\n ")
    op.print_matrix(Z, rounded=True)
    print('The reconstructed matrix based off of the latent representation is: \n')
    op.print_matrix(op.mat_multiply(Z,op.conjugate(V)), rounded=True)
    print(f'The average reconstruction error for this process was {op.avg_reconstruct_err(X, op.mat_multiply(Z,op.conjugate(V)))}.')

#This is simply the main line function
def main():
    #These two lines create a gloabal instance of the class object called op.
    global op
    op = lin_alg()
    #This generates a random gaussian matrix that is 40 by 20.
    mat =  op.random_matrix(40,20)
    print('Our original data matrix is: \n')
    op.print_matrix(mat, rounded=True)
    #These functions are descrbed above.
    SVD_example(mat)
    eig_decomp_example(mat)
    auto_encoder_decoder_example(mat)

main()
'''

