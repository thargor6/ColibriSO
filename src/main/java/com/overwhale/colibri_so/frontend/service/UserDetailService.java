package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.UserDetail;
import com.overwhale.colibri_so.backend.repository.UserDetailRepository;
import com.overwhale.colibri_so.frontend.dto.UserDetailDto;
import com.overwhale.colibri_so.frontend.mapper.UserDetailMapper;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.util.Optional;
import java.util.UUID;

@Service
public class UserDetailService extends CrudService<UserDetailDto, UUID> {
  private final UserDetailRepository repository;
  private final UserDetailMapper userDetailMapper;

  public UserDetailService(UserDetailRepository repository, UserDetailMapper userDetailMapper) {
    this.repository = repository;
    this.userDetailMapper = userDetailMapper;
  }

  public UserDetailDto update(UserDetailDto dto) {
    UserDetail entity = userDetailMapper.dtoToEntiy(dto);
    return userDetailMapper.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<UserDetailDto, UUID> getRepository() {
    return null;
  }

  public Optional<UserDetailDto> get(UUID id) {
    return repository.findById(id).map(e -> userDetailMapper.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<UserDetailDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> userDetailMapper.entityToDto(e));
  }

  public int count() {
    return (int) repository.count();
  }
}
