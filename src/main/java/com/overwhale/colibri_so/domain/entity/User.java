package com.overwhale.colibri_so.domain.entity;

import lombok.Data;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.lang3.RandomStringUtils;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Data
public class User extends BaseEntity {

  @NotNull
  private String username;

  private String passwordSalt;

  private String passwordHash;

  private String email;

  public void setPassword(String password) {
    this.passwordSalt = RandomStringUtils.random(32);
    this.passwordHash = DigestUtils.sha1Hex(password + passwordSalt);
  }

  public boolean cherckPassword(String refPassword) {
    return DigestUtils.sha1Hex(refPassword + this.passwordSalt).equals(this.passwordHash);
  }

}
